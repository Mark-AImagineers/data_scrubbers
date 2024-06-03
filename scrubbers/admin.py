from django.contrib import admin
from .models import Region, WeatherData, HourlyTemperature, PoliticalNews

# Register your models here.
admin.site.register(Region)
admin.site.register(WeatherData)
admin.site.register(HourlyTemperature)
admin.site.register(PoliticalNews)