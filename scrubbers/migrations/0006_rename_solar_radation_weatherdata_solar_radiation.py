# Generated by Django 5.0.6 on 2024-05-30 13:27

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('scrubbers', '0005_alter_weatherdata_cloud_cover_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='weatherdata',
            old_name='solar_radation',
            new_name='solar_radiation',
        ),
    ]