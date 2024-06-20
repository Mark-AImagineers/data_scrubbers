from django.contrib import admin
from .models import Region, WeatherData, HourlyTemperature, PoliticalNews, BusinessNews, BusNews_Metrics

# Register your models here.
admin.site.register(Region)
admin.site.register(WeatherData)
admin.site.register(HourlyTemperature)
admin.site.register(PoliticalNews)
admin.site.register(BusinessNews)
admin.site.register(BusNews_Metrics)