from django.shortcuts import render, redirect
from django.http import JsonResponse
from .config import api_key
from .models import Region, WeatherData, HourlyTemperature, PoliticalNews
import requests
from django.contrib import messages
from django.shortcuts import render
from webdriver_manager.chrome import ChromeDriverManager
from django.core.exceptions import ObjectDoesNotExist
import requests as re
import logging
from django.contrib import messages
from .tasks import *


logger = logging.getLogger('data_scrub_log')

print(f"-----Started Django Server-----")
logger.info(f"-----Started Django Server-----")

## FUNCTIONS

## VIEWS

def index(request):
    return render(request, 'index.html')

def weather_scrubber(request):
    logger.info("User navigated to weather scrubber page")
    if request.method == 'POST':
        logger.info("Weather Scrubber POST request received")
        startdate = request.POST['date1']
        enddate = request.POST['date2']
        logger.info(f"Data recieived: {startdate} to {enddate}!")
        scrub_weather_data.delay(startdate, enddate)
        messages.info(request, f"Weather data scrubbing started for {startdate} to {enddate}!")
        return redirect('weather_scrubber')
    else:
        return render(request, 'weather_scrubber.html')
                            
def manage_regions(request):
    if request.method == 'POST':
        logger.info("Manage Regions POST request received")
        region_name = request.POST['region_name']
        region_country = request.POST['region_country']
        region_center = request.POST['region_center']
        region_lat = request.POST['region_lat']
        region_lon = request.POST['region_lon']
        new_region = Region(name=region_name, country=region_country, regional_center=region_center, latitude=region_lat, longitude=region_lon)
        new_region.save()
        logger.info(f"Region {region_name} successfully created!")

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
    logger.info(f"Region {entry.name} successfully deleted!")
    return redirect('manage_regions')

def politics_scrubber(request):
    return render(request, 'political_scrubber.html')

def test_environment(request):
    result = add.delay(4,5)
    logger.info(f"Result = {result.get()}")
    return render(request, 'test_environment.html')