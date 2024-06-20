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

## V0.3.4
- implemented technology scraper with inquirer scraper

## V0.3.3
- decided to skip PNA scraper for now. 403 on testing. Might need headers.
- completed business news with inquirer scraper

## V0.3.2
- successfully connect celery-django and scrapy
- inquirerscrapy now working - added basic logs - need further refinement
- now able to Scrape author, publication date

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
- Add scheduled run for Weather Scrubbers
- Create Auto Backup of Weather Scrubbers data
- Add check - unable to put weather data end date < start date
- need to improve query time (SQL Cache?)
- improve notifications on celery tasks (get best practice)
- improve logger - lessen verbose, add more logs for scrapy logic
- PNA Scanner for political news (adding diversity to news sources)
- need to clean data source - remove unreadable text


## NOTES
- Technology through inquirer.net only has 219 pages. - will scrub this as soon as its working and latest news will always be on page 1.



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

------------