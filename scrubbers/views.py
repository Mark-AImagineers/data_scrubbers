from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.contrib import messages
from django.shortcuts import render
from webdriver_manager.chrome import ChromeDriverManager
from django.core.exceptions import ObjectDoesNotExist
from django.contrib import messages
from celery.result import AsyncResult
from django.contrib import messages
from django.apps import apps
from django.contrib.auth.decorators import login_required, permission_required
from django.utils import timezone

import requests
import os
import csv
import requests as re
import logging

from .config import api_key
from .models import *
from .tasks import *
from .forms import ScraperForm, BusinessForm, TechnologyForm
from .tasks import run_scrapy_spider


logger = logging.getLogger('data_scrub_log')

print(f"-----Started Django Server-----")
logger.info(f"-----Started Django Server-----")

db_to_url_name = {
    'PoliticalNews': 'politics_scrubber',
    'BusinessNews': 'business_scrubber',
    'TechnologyNews': 'technology_scrubber',
    'WeatherData': 'weather_scrubber',
    'None': 'index'
}

db_to_metrics = {
    'PoliticalNews': (PolNews_Metrics, 'political_news'),
    'BusinessNews': (BusNews_Metrics,'business_news'),
    'TechnologyNews': (TechNews_Metrics, 'technology_news'),
}

db_to_model = {
    'PoliticalNews': PoliticalNews,
    'BusinessNews': BusinessNews,
    'TechnologyNews': TechnologyNews,
}


## FUNCTIONS

def manage_task_session(request, task_type, async_task):
    request.session['current_task'] = {'id': async_task.id, 'type': task_type}
    request.session['message_added'] = False

def check_and_manage_task(request):
    task_info = request.session.get('current_task', None)
    message_added = request.session.get('message_added', False)
    
    if task_info:
        result = AsyncResult(task_info['id'])
        if result.ready() and not message_added:
            messages.info(request, f"{task_info['type']} scrubber task {task_info['id']} completed!")
            request.session.pop('current_task')
            request.session['message_added'] = True
            return None
        elif not result.ready() and not message_added:
            messages.info(request, f"{task_info['type']} scrubber task {task_info['id']} is still running.")
            request.session['message_added'] = True
        return task_info
    return None

## VIEWS
def test_environment(request):
    return render(request, 'test_environment.html')
def index(request):
    return render(request, 'index.html')

def weather_scrubber(request):
    request.session['db_type'] = 'WeatherData'
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
    request.session['db_type'] = 'PoliticalNews'
    form = ScraperForm()
    if request.method == 'POST':
        form = ScraperForm(request.POST)
        if form.is_valid():
            scraper_type = form.cleaned_data['scraper_type']
            start_page = form.cleaned_data['start_page']
            end_page = form.cleaned_data['end_page']
            
            async_task = run_scrapy_spider.delay(scraper_type, start_page, end_page)
            manage_task_session(request, scraper_type, async_task)
            return redirect('politics_scrubber')
        else:
            return render(request, 'political_scrubber.html', {'form': form})
    else:
        if check_and_manage_task(request) is None:
            request.session['message_added'] = False
        return render(request, 'political_scrubber.html', {'form': form})

def business_scrubber(request):
    request.session['db_type'] = 'BusinessNews'
    form = BusinessForm()
    if request.method == 'POST':
        form = BusinessForm(request.POST)
        if form.is_valid():
            scraper_type = form.cleaned_data['scraper_type']
            start_page = form.cleaned_data['start_page']
            end_page = form.cleaned_data['end_page']
            
            async_task = run_scrapy_spider.delay(scraper_type, start_page, end_page)
            manage_task_session(request, scraper_type, async_task)
            return redirect('business_scrubber')
        else:
            return render(request, 'business_scrubber.html', {'form': form})
    else:
        if check_and_manage_task(request) is None:
            request.session['message_added'] = False
        return render(request, 'business_scrubber.html', {'form': form})


def technology_scrubber(request):
    request.session['db_type'] = 'TechnologyNews'
    form = TechnologyForm()
    if request.method == 'POST':
        form = TechnologyForm(request.POST)
        if form.is_valid():
            scraper_type = form.cleaned_data['scraper_type']
            start_page = form.cleaned_data['start_page']
            end_page = form.cleaned_data['end_page']
            
            async_task = run_scrapy_spider.delay(scraper_type, start_page, end_page)
            manage_task_session(request, scraper_type, async_task)
            return redirect('technology_scrubber')
        else:
            return render(request, 'technology_scrubber.html', {'form': form})
    else:
        if check_and_manage_task(request) is None:
            request.session['message_added'] = False
        return render(request, 'technology_scrubber.html', {'form': form})
    

@login_required
@permission_required('app.view_model', raise_exception=True)
def export_to_csv(request):
    db_type = request.session.get('db_type', None)
    redirect_url = db_to_url_name[db_type]
    logger.info(f"DB TYPE: {db_type}")
    messages.info(request, f"PENDING: Exporting {db_type} DB to CSV...")

    csv_dir = "./csv/"

    if not os.path.exists(csv_dir):
        os.makedirs(csv_dir)
        logger.info(f"Created {csv_dir}")

    try:
        model = apps.get_model('scrubbers', db_type)
        logger.info(f"Using {model} model")
    except LookupError:
        messages.error(request, "Invalid model type provided")
        logger.info(f"Invalid model type provided")
        return redirect(redirect_url)
    
    filename = os.path.join(csv_dir, f"{db_type}.csv")
    with open(filename, 'w', newline='') as file:
        writer = csv.writer(file)
        headers = [field.name for field in model._meta.fields]
        writer.writerow(headers)
        for instance in model.objects.all():
            writer.writerow([getattr(instance, field) for field in headers])

    logger.info(f"Exported {db_type} DB to {csv_dir}")
    messages.info(request, f"SUCCESS: Exported {db_type} DB to {csv_dir}")               

    
    return redirect(redirect_url)

@login_required
def summarize_news(request):
    from transformers import pipeline
    summarizer = pipeline("summarization", model="facebook/bart-large-cnn")
    db_type = request.session.get('db_type', None)
    redirect_url = db_to_url_name[db_type]

    if db_type not in db_to_model:
        messages.error(request, "Invalid model type provided")
        logger.info(f"Invalid model type provided")
        return redirect(redirect_url)
    
    ModelClass = db_to_model[db_type]
    MetricsClass, fk_field = db_to_metrics[db_type]
    news_articles = ModelClass.objects.all()

    logger.info(f"DB TYPE: {db_type}")
    messages.info(request, f"PENDING: Sumarizing all {db_type} entries...")   

    for article in news_articles:
        if article.full_text:
            try:
                summary_result = summarizer(article.full_text, max_length=130, min_length=30, do_sample=False)
                if summary_result:
                    summary_text = summary_result[0]['summary_text']
                    metrics_instance, created = MetricsClass.objects.get_or_create(**{fk_field: article})
                    metrics_instance.summary = summary_text
                    metrics_instance.updated_at = timezone.now()
                    metrics_instance.save()
                    logger.info("Successfully summarized article ID: %s", article.id)
                    messages.info(f"SUCCESS: Summarized article {article.id}")
            except Exception as e:
                logger.error("Error summarizing article ID: %s: %s", article.id, str(e))
                messages.error(request, f"Error summarizing article {article.id}: {str(e)}")


    messages.info(request, f"COMPLETED: Summarized all {db_type} entries")
    return redirect(redirect_url)