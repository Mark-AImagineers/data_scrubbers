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
from celery.result import AsyncResult
from .forms import ScraperForm, BusinessForm, TechnologyForm
from .tasks import run_scrapy_spider
from django.contrib import messages


logger = logging.getLogger('data_scrub_log')

print(f"-----Started Django Server-----")
logger.info(f"-----Started Django Server-----")

## FUNCTIONS

## VIEWS
def test_environment(request):
    return render(request, 'test_environment.html')
def index(request):
    return render(request, 'index.html')

def weather_scrubber(request):
    logger.info("User navigated to weather scrubber page")
    if request.method == 'POST':
        logger.info("Weather Scrubber POST request received")
        startdate = request.POST['date1']
        enddate = request.POST['date2']
        logger.info(f"Data recieived: {startdate} to {enddate}!")
        async_task = scrub_weather_data.delay(startdate, enddate)
        task_id = async_task.id
        messages.info(request, f"Weather scrubber task {task_id} started")
        logger.info(f"Weather scrubber task {task_id} started")
        request.session['task_id'] = task_id
        return redirect('weather_scrubber')
    else:
        task_id = request.session.get('task_id', None)

        if task_id:
            result = AsyncResult(task_id)
            if result.ready():
                messages.info(request, f"Weather scrubber task {task_id} completed!")
                del request.session['task_id']
            else:
                messages.info(request, f"Weather scrubber task {task_id} is still running")
        else:
            messages.info(request, f"No weather scrubber task is running")
            request.session['task_id'] = None
        
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
    form = ScraperForm()
    if request.method == 'POST':
        form = ScraperForm(request.POST)
        if form.is_valid():
            scraper_type = form.cleaned_data['scraper_type']
            start_page = form.cleaned_data['start_page'] 
            end_page = form.cleaned_data['end_page']

            run_scrapy_spider.delay(scraper_type, start_page, end_page)
            messages.success(request, "Scraper has been started!")
            return redirect('politics_scrubber')
        
        else:
            return render(request, 'political_scrubber.html', {'form': form})
        
    return render(request, 'political_scrubber.html', {'form': form})

def business_scrubber(request):
    form = BusinessForm()
    if request.method == 'POST':
        form = BusinessForm(request.POST)
        if form.is_valid():
            scraper_type = form.cleaned_data['scraper_type']
            start_page = form.cleaned_data['start_page'] 
            end_page = form.cleaned_data['end_page']

            run_scrapy_spider.delay(scraper_type, start_page, end_page)
            messages.success(request, "Scraper has been started!")
            return redirect('business_scrubber')
        
        else:
            return render(request, 'business_scrubber.html', {'form': form})
    
    return render(request, 'business_scrubber.html', {'form': form})


def technology_scrubber(request):
    form = TechnologyForm()
    if request.method == 'POST':
        form = TechnologyForm(request.POST)
        if form.is_valid():
            scraper_type = form.cleaned_data['scraper_type']
            start_page = form.cleaned_data['start_page'] 
            end_page = form.cleaned_data['end_page']

            run_scrapy_spider.delay(scraper_type, start_page, end_page)
            messages.success(request, "Scraper has been started!")
            return redirect('technology_scrubber')
        
        else:
            return render(request, 'technology_scrubber.html', {'form': form})
    
    return render(request, 'technology_scrubber.html', {'form': form})
