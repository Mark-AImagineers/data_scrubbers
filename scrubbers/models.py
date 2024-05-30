from django.db import models

# Create your models here.
class Region(models.Model):
    name = models.CharField(max_length=255)
    country = models.CharField(max_length=255, default='Philippines')
    regional_center = models.CharField(max_length=255, null=True)
    latitude = models.FloatField()
    longitude = models.FloatField()

    def __str__(self):
        return self.name
class WeatherData(models.Model):
    region = models.ForeignKey(Region, on_delete=models.CASCADE)
    datetime = models.DateTimeField()
    temp = models.FloatField()
    feels_like = models.FloatField(null=True, blank=True)
    humidity = models.IntegerField(null=True, blank=True)
    dew_point = models.FloatField(null=True, blank=True)
    precipitation = models.FloatField(null=True, blank=True)
    precipitation_prob = models.FloatField(null=True, blank=True)
    snow = models.FloatField(null=True, blank=True)
    snow_depth = models.FloatField(null=True, blank=True)
    wind_gust = models.FloatField(null=True, blank=True)
    wind_speed = models.FloatField(null=True, blank=True)
    wind_direction = models.FloatField(null=True, blank=True)
    pressure = models.FloatField(null=True, blank=True)
    visibility = models.FloatField(null=True, blank=True)
    cloud_cover = models.IntegerField(null=True, blank=True)
    solar_radiation = models.FloatField(null=True, blank=True)
    solar_energy = models.FloatField(null=True, blank=True)
    uv_index = models.IntegerField(null=True, blank=True)
    severe_risk = models.IntegerField(null=True, blank=True)
    conditions = models.CharField(max_length=255, null=True, blank=True)
    icon = models.CharField(max_length=50, null=True, blank=True)

    def __str__(self):
        return f"Weather Data for {self.region.name} on {self.datetime.strftime('%Y-%m-%d %H:%M:%S')}"
    
class HourlyTemperature(models.Model):
    weather_data = models.ForeignKey(WeatherData, on_delete=models.CASCADE)
    hour = models.IntegerField()
    temperature = models.FloatField()

    def __str__(self):
        return f"{self.temperature}°C at {self.hour}:00 on {self.weather_data.datetime.strftime('%Y-%m-%d')}"