from django.contrib import admin
from django.urls import path
from .views import *

urlpatterns = [
    path('weather/', weather_scrubber, name='weather_scrubber'),
    path('manage_regions/', manage_regions, name='manage_regions'),
    path('delete/<int:regional_id>/',delete_entry, name='delete_entry'),
]
