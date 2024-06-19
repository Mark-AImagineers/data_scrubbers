from celery import shared_task
from django.conf import settings
import requests as re
import logging
from .models import *
from .config import api_key
from django.db import transaction
import subprocess
import os

logger = logging.getLogger('data_scrub_log')

def build_api_url(lat, lon, date1, date2, api_key):
    base_url = "https://weather.visualcrossing.com/VisualCrossingWebServices/rest/services/timeline/"
    location = f"{lat},{lon}/"
    startdate = f"{date1}/"
    enddate = f"{date2}/"
    query_params = "?unitGroup=metric&include=days%2Chours%2Calerts%2Ccurrent%2Cevents&contentType=json"
    if date1==date2:
        date2 = ""
        
    if date2=="":
        api_url = f"{base_url}{location}{startdate}{query_params}&key={api_key}"
    else:
        api_url = f"{base_url}{location}{startdate}{enddate}{query_params}&key={api_key}"
    return api_url

@shared_task(bind=True, max_retries=3)
def scrub_weather_data(self, startdate, enddate):
    regions = Region.objects.all()
    API = api_key
    for region in regions:
        url = build_api_url(region.latitude, region.longitude, startdate, enddate, API)
        logger.info(f"Scrubbing weather for {region.name} from {startdate} to {enddate}...")
        response = re.get(url)
        if response.status_code == 200:
            data = response.json()
            logger.info(f"Length of data received: {len(data)}")
            
            for day in data.get('days', []):
                try:
                    with transaction.atomic():
                        exists = WeatherData.objects.filter(
                        region=region, 
                        datetime=day['datetime']
                        ).exists()
                    
                        if not exists:
                            weather_entry = WeatherData(
                                region=region,
                                datetime=day['datetime'],
                                temp=day['temp'],
                                feels_like=day['feelslike'],
                                humidity=day['humidity'],
                                dew_point=day['dew'],
                                precipitation=day['precip'],
                                precipitation_prob=day['precipprob'],
                                snow=day['snow'],
                                snow_depth=day['snowdepth'],
                                wind_gust=day['windgust'],
                                wind_speed=day['windspeed'],
                                wind_direction=day['winddir'],
                                pressure=day['pressure'],
                                visibility=day['visibility'],
                                cloud_cover=day['cloudcover'],
                                solar_radiation=day['solarradiation'],
                                solar_energy=day['solarenergy'],
                                uv_index=day['uvindex'],
                                severe_risk=day.get('severerisk', 0),
                                conditions=day['conditions'],
                                icon=day['icon'],
                            )
                            weather_entry.save()

                            logger.info(f"Weather data for {region.name} on {day['datetime']} successfully scrubbed!")

                            count_hourly_temp_entries = 0

                            for hour in day.get('hours', []):
                                HourlyTemperature.objects.create(
                                    weather_data=weather_entry,
                                    hour=int(hour['datetime'].split(':')[0]),  # Extracting the hour part
                                    temperature=hour['temp'],
                                )
                                count_hourly_temp_entries += 1
                            
                            logger.info(f"Total hourly temperature entries created: {count_hourly_temp_entries}")
                        else:
                            logger.info(f"Weather data for {region.name} on {day['datetime']} already exists... Skipping...")

                except Exception as exc:
                    logger.error(f"Error: {exc}")
                    self.retry(exc=exc)

        else:
            logger.error(f"Error fetching data for {region.name} with status code {response.status_code}.")
    logger.info(f"Completed all weather data scrubbing!")
    return True
@shared_task
def run_scrapy_spider(scraper_type, start_page, end_page):
    current_directory = os.getcwd()
    logger.info(f"Current directory is {current_directory}")
    project_path = os.path.join('/usr/src/app/', 'articlescraper')
    logger.info(f"Project path is {project_path}")

    try:
        if current_directory!= project_path:
            os.chdir(project_path)
            logger.info(f"Changed directory to {project_path}")
            print(f"Changed directory to {project_path}")
        else:
            logger.info(f"Current directory is {current_directory}")
            print("No changes in directory")
    except FileNotFoundError:
        logger.error(f"Failed to change directory to {project_path}. Directory not found.")
        print(f"Failed to change directory to {project_path}. Directory not found.")
        return "Directory not found."

    command = f'scrapy crawl {scraper_type} -a start_page={start_page} -a end_page={end_page}'

    process = subprocess.Popen(
        command,
        shell=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE
    )

    stdout, stderr = process.communicate()

    if process.returncode == 0:
        logger.info(f"Scrapy spider {scraper_type} completed successfully!")
        print(f"Scrapy spider {scraper_type} completed successfully!")
        return stdout.decode()
    else:
        print(f"Error running scrapy spider {scraper_type}")
        logger.error(f"Error running scrapy spider {scraper_type}")
        return stderr.decode()
    

