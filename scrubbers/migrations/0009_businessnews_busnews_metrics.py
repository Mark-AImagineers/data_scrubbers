# Generated by Django 5.0.6 on 2024-06-19 10:40

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('scrubbers', '0008_alter_hourlytemperature_temperature_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='BusinessNews',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(blank=True, max_length=255, null=True)),
                ('author', models.CharField(blank=True, max_length=255, null=True)),
                ('publication_date', models.DateTimeField(blank=True, null=True)),
                ('source', models.CharField(blank=True, max_length=255, null=True)),
                ('url', models.URLField(blank=True, null=True)),
                ('full_text', models.TextField(blank=True, null=True)),
                ('country', models.CharField(blank=True, max_length=255, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='BusNews_Metrics',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('summary', models.CharField(blank=True, max_length=255, null=True)),
                ('sentiment_score', models.FloatField(blank=True, null=True)),
                ('sentiment_classification', models.CharField(blank=True, max_length=255, null=True)),
                ('named_entities', models.CharField(blank=True, max_length=255, null=True)),
                ('key_phrases', models.TextField(blank=True, null=True)),
                ('engagement_metrics', models.JSONField(blank=True, null=True)),
                ('updated_at', models.DateTimeField(blank=True, null=True)),
                ('business_news', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='scrubbers.businessnews')),
            ],
        ),
    ]
