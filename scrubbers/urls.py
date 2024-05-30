from django.contrib import admin
from django.urls import path
from .views import *

urlpatterns = [
    path('weather/', weather_scrubber, name='weather_scrubber'),
]
