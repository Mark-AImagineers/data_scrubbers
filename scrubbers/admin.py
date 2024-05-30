from django.contrib import admin
from .models import Region, WeatherData, HourlyTemperature

# Register your models here.
admin.site.register(Region)
admin.site.register(WeatherData)
admin.site.register(HourlyTemperature)