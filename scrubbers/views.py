from django.shortcuts import render, redirect
from django.http import JsonResponse
from .config import api_key
from .models import Region, WeatherData, HourlyTemperature, PoliticalNews
import requests
from django.contrib import messages
from django.shortcuts import render
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from django.core.exceptions import ObjectDoesNotExist

## FUNCTIONS

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

class BaseScraper:
    def __init__(self):
        self.driver = self.init_driver()
    
    def init_driver(self):
        chrome_options = Options()
        chrome_options.add_experimental_option('excludeSwitches', ['enable-logging'])
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument("--window-size=1920,1080")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--remote-debugging-port=9222")
        chrome_options.add_argument("--disable-extensions")
        chrome_options.add_argument("--disable-popup-blocking")
        chrome_options.add_argument("--disable-notifications")
        chrome_options.add_argument("--disable-infobars")
        chrome_options.add_argument("--disable-logging")
        chrome_options.add_argument("--log-level=3")
        chrome_options.add_argument("--disable-blink-features=AutomationControlled")
        chrome_options.add_argument("--disable-third-party-cookies")
        service = Service(ChromeDriverManager().install())
        return webdriver.Chrome(service=service, options=chrome_options)
    
    def save_article_data(article_data):
        try:
            existing_article = PoliticalNews.objects.get(url=article_data['url'])
            print("Article already exists. Skipping...")
        except ObjectDoesNotExist:
            political_news = PoliticalNews(
                title = article_data['title'],
                author = article_data['author'],
                publication_date = article_data['publication_date'],
                source = article_data['source'],
                url = article_data['url'],
                full_text = article_data['full_text'],
                country = article_data['country'],
            )
            political_news.save()
            print(f"Successfully saved: {article_data['url']}")


    def close_driver(self):
        self.driver.quit()

    def scrape(self):
        raise NotImplementedError("This method should be implemented by subclass.")

class InquirerScraper(BaseScraper):
    def get_article_links(self, target_urls):
        article_links = []
        for url in target_urls:
            self.driver.get(url)
            WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, 'a[href^="https://newsinfo.inquirer.net/"]'))
            )
            
            links = self.driver.find_elements(By.CSS_SELECTOR, 'a[href^="https://newsinfo.inquirer.net/"]')
            page_links = [link.get_attribute('href') for link in links if 'newsinfo.inquirer.net' in link.get_attribute('href')]
            article_links.extend(page_links)
        return list(set(article_links))
    
    def get_article_text(self, url):
        self.driver.get(url)
        WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.ID, 'art_body_wrap'))
        )
        title = self.driver.title
        paragraphs = self.driver.find_elements(By.CSS_SELECTOR, '#art_body_wrap #article_content p')
        article_text = '\n'.join([para.text for para in paragraphs])
        
        author = None  # Implement logic at a later stage"
        publication_date = None  # Implement logic at a later stage"
        country = "Philippines"
        
        return {
            "title": title,
            "author": author,
            "publication_date": publication_date,
            "url": url,
            "full_text": article_text,
            "source": "Inquirer",
            "country": country
        }
    
    def scrape(self, target_urls):
        links = self.get_article_links(target_urls)
        for url in links:
            article_data = self.get_article_text(url)
            self.save_article_data(article_data)
    

class PNAScraper(BaseScraper):
    def get_article_links(self, target_urls):
        # PNA-Specific logic here - BS4
        pass

    def get_article_text(self, url):
        # PNA-Specific logic here - BS4
        pass

    def scrape(self, target_urls):
        links = self.get_article_links(target_urls)
        for url in links:
            article_data = self.get_article_text(url)
            self.save_article_data(article_data)


## VIEWS

def index(request):
    return render(request, 'index.html')

def weather_scrubber(request):
    if request.method == 'POST':
        regions = Region.objects.all()
        API = api_key
        startdate = request.POST['date1']
        enddate = request.POST['date2']
        print(f"{startdate} to {enddate}")

        for region in regions:
            url = build_api_url(region.latitude, region.longitude, startdate, enddate, API)
            response = requests.get(url)
            if response.status_code == 200:
                data = response.json()
                print(data)
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
                        #Error handling here    

                        for hour in day.get('hours', []):
                            HourlyTemperature.objects.create(
                                weather_data=weather_entry,
                                hour=int(hour['datetime'].split(':')[0]),  # Extracting the hour part
                                temperature=hour['temp'],
                            )
                            #error handling here
                    else:
                        print(f"Weather data for {region.name} on {day['datetime']} already exists. Skipping...")
            else:
                messages.error(request, f"Error fetching data for {region.name} with status code {response.status_code}.")
                return redirect('weather_scrubber')
        
        messages.success(request, 'Weather data successfully scrubbed!')
        return redirect('weather_scrubber')

    else:
        return render(request, 'weather_scrubber.html')
                    
def manage_regions(request):
    if request.method == 'POST':
        region_name = request.POST['region_name']
        region_country = request.POST['region_country']
        region_center = request.POST['region_center']
        region_lat = request.POST['region_lat']
        region_lon = request.POST['region_lon']
        new_region = Region(name=region_name, country=region_country, regional_center=region_center, latitude=region_lat, longitude=region_lon)
        new_region.save()

        regions = Region.objects.all()
        context = {'regions': regions}
        return render(request,'manage_weather_regions.html',context)
    else:
        regions = Region.objects.all()
        context = {'regions': regions}
        return render(request,'manage_weather_regions.html', context)

def delete_entry(request, regional_id):
    entry = Region.objects.get(id=regional_id)
    entry.delete()
    return redirect('manage_regions')

def politics_scrubber(request):
    if request.method == 'POST':
        scraper_type = request.POST.get('scraper_type', 'Inquirer')

        if scraper_type == 'Inquirer':
            scraper = InquirerScraper()
        elif scraper_type == 'PNA':
            scraper = PNAScraper()
        else:
            return JsonResponse({'error': 'Invalid scraper type.'}, status=400)
        
        start_page = request.POST.get('page_num1', '')
        end_page = request.POST.get('page_num2','')

        if not start_page:
            target_urls = ["https:/"]







