from celery import shared_task
from django.conf import settings
import requests as re
import logging
from .models import *
from .config import api_key

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

@shared_task
def scrub_weather_data(startdate, enddate):
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

                    for hour in day.get('hours', []):
                        HourlyTemperature.objects.create(
                            weather_data=weather_entry,
                            hour=int(hour['datetime'].split(':')[0]),  # Extracting the hour part
                            temperature=hour['temp'],
                        )
                        logger.info(f"Hourly temperature for {region.name} on {day['datetime']} successfully scrubbed!")
                    else:
                        logger.info(f"Weather data for {region.name} on {day['datetime']} already exists")
        else:
            logger.error(f"Error fetching data for {region.name} with status code {response.status_code}.")
    logger.info(f"Completed all weather data scrubbing!")

@shared_task
def add(x,y):
    result = x + y
    logger.info(f"Adding {x} + {y} = {result}")
    return result