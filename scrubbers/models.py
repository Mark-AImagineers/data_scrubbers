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
    temp = models.FloatField(null=True, blank=True)
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
    temperature = models.FloatField(null=True, blank=True)

    def __str__(self):
        return f"{self.temperature}°C at {self.hour}:00 on {self.weather_data.datetime.strftime('%Y-%m-%d')}"

   
class PoliticalNews(models.Model):
    title = models.CharField(max_length=255, null=True, blank=True)
    author = models.CharField(max_length=255, null=True, blank=True)
    publication_date = models.DateTimeField(null=True, blank=True)
    source = models.CharField(max_length=255, null=True, blank=True)
    url = models.URLField(null=True, blank=True)
    full_text = models.TextField(null=True, blank=True)
    country = models.CharField(max_length=255, null=True, blank=True)

    def __str__(self):
        return f"{self.country} - {self.title}"
    
class PolNews_Metrics(models.Model):
    political_news = models.ForeignKey(PoliticalNews, on_delete=models.CASCADE)
    summary = models.CharField(max_length=255, null=True, blank=True)
    sentiment_score = models.FloatField(null=True, blank=True)
    sentiment_classification = models.CharField(max_length=255, null=True, blank=True)
    named_entities = models.CharField(max_length=255, null=True, blank=True)
    key_phrases = models.TextField(null=True, blank=True)
    engagement_metrics = models.JSONField(null=True, blank=True)
    updated_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"{self.political_news.title} by {self.political_news.author} on {self.political_news.publication_date.strftime('%Y-%m-%d %H:%M:%S')}"

