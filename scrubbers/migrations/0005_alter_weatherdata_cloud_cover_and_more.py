# Generated by Django 5.0.6 on 2024-05-30 13:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('scrubbers', '0004_rename_latitue_region_latitude'),
    ]

    operations = [
        migrations.AlterField(
            model_name='weatherdata',
            name='cloud_cover',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='weatherdata',
            name='conditions',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='weatherdata',
            name='dew_point',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='weatherdata',
            name='feels_like',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='weatherdata',
            name='humidity',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='weatherdata',
            name='icon',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='weatherdata',
            name='precipitation',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='weatherdata',
            name='precipitation_prob',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='weatherdata',
            name='pressure',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='weatherdata',
            name='severe_risk',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='weatherdata',
            name='solar_radation',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='weatherdata',
            name='uv_index',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='weatherdata',
            name='visibility',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='weatherdata',
            name='wind_direction',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='weatherdata',
            name='wind_gust',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='weatherdata',
            name='wind_speed',
            field=models.FloatField(blank=True, null=True),
        ),
    ]
