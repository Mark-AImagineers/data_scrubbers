# Generated by Django 5.0.6 on 2024-06-06 05:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('scrubbers', '0007_politicalnews_polnews_metrics'),
    ]

    operations = [
        migrations.AlterField(
            model_name='hourlytemperature',
            name='temperature',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='weatherdata',
            name='temp',
            field=models.FloatField(blank=True, null=True),
        ),
    ]
