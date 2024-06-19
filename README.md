# DATA SCRUBBERS PROJECT

## Project Overview
This project aims to collect and scrub extensive and valuable data for future machine learning (ML) projects, with a focus on business-related cases. The project is also intended to generate revenue by selling the curated and enriched datasets.

## Scrubbers
The project utilizes various data scrubbers to gather information from different sources, categorized as follows:
- **Political News**
- **Business News**
- **Business Magazine Articles**
- **Marketing Data**
- **Weather Data**
- **Legal News and Regulations**

These scrubbers are designed to perform a PESTLE analysis, ensuring comprehensive coverage of Political, Economic, Social, Technological, Legal, and Environmental factors.

## Data Sources
The data is collected from a variety of sources, including news websites, business magazines, weather services, and legal databases.

## Architecture
The project is built using Django for the backend and PostgreSQL for the database. The architecture is designed to support local deployment while being future-proofed for potential deployment on platforms like Heroku.

## Deployment
To deploy the project locally, follow these steps:
1. Clone the repository.
2. Install the necessary dependencies.
3. Set up the PostgreSQL database.
4. Run the Django server.

Detailed setup instructions will be provided below.

## Dependencies
The primary dependencies for this project include:
- Django
- PostgreSQL
- Django REST framework (for building APIs)
- Additional libraries as needed for specific data sources and scrubbing tasks.

## Usage
Users can interact with the project through a RESTful API, which allows them to initiate data scrubbing tasks, retrieve scrubbed data, and manage the data collection process.

## Future Plans
Future enhancements and planned features include:
- Additional scrubbers for more data sources.
- Improved data cleaning and enrichment algorithms.
- Enhanced user interface for managing scrubbing tasks.
- Deployment on cloud platforms like Heroku.

# Version History

## V0.3.2
- attempting to connect celery-django and scrapy

## V0.3.1
- Partially able to run scrapy logic for inquirer.net Nation landing page
- need to create a solution where im able to add page and start the scraping logic from there
- from here we need to send this to celery for asynchonous handling and connect it through django - will start a new branch for this dev.


## V0.3.0
- Implemented Dockers (Django, Redis, Celery)
- Weather Data Scrubbing working in Celery
- Implemenent Logging System

## V0.2.0
- started working on the Political News Scrub - completed
- add check before saving political data to DB - unique entries only
- remove 3rd party cookies warning

## V0.1.2
- added check before saving weather data to DB - Unique entries only

## V0.1.1
- Weather Scrubbers now working

## V0.1.0
- Initialise Project
- Started woring on a simple UI

## Pending


## Pipeline
- Scraping author, publication date
- Add scheduled run for Weather Scrubbers
- Create Auto Backup of Weather Scrubbers data
- Add check - unable to put weather data end date < start date
- need to improve query time (SQL Cache?)
- improve notifications on celery tasks (get best practice)
- improve logger - lessen verbose






## Journal

Weather API is now working
Needs further refinement. Need to make sure duplicate records are not allowed in DB.
Create a way to pause the app midway through run
- use this idea to check for pause state everytime the program finishes a cycle.

-----------------
Duplicate records are check during weather fetching.

Making the pause the app midway through needs a bit more thought and I think i'll push this at a later date when refining the function

for now i need to work on being able to code the other parts of the app so i have a functional multi purpose scrubber

but for instructions we'd be using Celery and here's how.

Asynchronous Task Management with Celery in Django
This guide describes how to set up and use Celery with Django to handle long-running tasks without blocking the web server, allowing for real-time control over these tasks.

Requirements
Django
Celery
Redis (or another message broker supported by Celery)
Installation
Step 1: Install Necessary Packages
Install Celery and Redis (if not already installed). Redis will serve as the message broker for Celery.

bash
Copy code
pip install celery redis
Step 2: Configure Celery
Create a file named celery.py in your main Django project directory (where settings.py is located):

python
Copy code
from __future__ import absolute_import, unicode_literals
import os
from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'your_project.settings')

app = Celery('your_project')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()
Add Celery configuration to your settings.py:

python
Copy code
CELERY_BROKER_URL = 'redis://localhost:6379/0'
CELERY_RESULT_BACKEND = 'redis://localhost:6379/0'
Step 3: Define Celery Tasks
Define a task in your Django app in a file named tasks.py:

python
Copy code
from celery import shared_task
from django.core.cache import cache

@shared_task
def fetch_and_store_weather_data(start_year, end_year, api_key):
    for year in range(start_year, end_year + 1):
        if cache.get('stop_app'):
            print("Stopping the task as requested.")
            break
        print(f"Processing data for the year: {year}")
        # Add your data processing logic here
        cache.set('stop_app', False)
Step 4: Create Views to Control Tasks
Create views to start and stop the Celery tasks:

python
Copy code
from django.http import JsonResponse
from .tasks import fetch_and_store_weather_data
from django.core.cache import cache

def start_task(request):
    fetch_and_store_weather_data.delay(1990, 2024, 'your_api_key')
    return JsonResponse({"status": "Task started"})

def stop_task(request):
    cache.set('stop_app', True)
    return JsonResponse({"status": "Task will stop after current cycle"})
Step 5: Setup Redis
Ensure Redis is installed and running as it is required for Celery's message broker:

bash
Copy code
# Install Redis using your system's package manager, for example:
sudo apt-get install redis-server
# Ensure Redis is running
redis-server
Step 6: Integrate Front-End Controls
Add buttons on your frontend to call the start and stop views. This can be achieved with simple AJAX calls:

html
Copy code
<button onclick="startTask()">Start Task</button>
<button onclick="stopTask()">Stop Task</button>

<script>
function startTask() {
    fetch('/start-task').then(response => response.json()).then(data => alert(data.status));
}

function stopTask() {
    fetch('/stop-task').then(response => response.json()).then(data => alert(data.status));
}
</script>
Running the Project
Ensure your Django project is configured correctly, and start the Celery worker:

bash
Copy code
celery -A your_project worker --loglevel=info
Now, your project is set up to handle long-running asynchronous tasks with the ability to control these tasks dynamically through your web application.

---------------------