# Generated by Django 2.0.7 on 2018-07-12 14:12

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('geostore', '0011_auto_20180711_0831'),
    ]

    operations = [
        migrations.RunSQL("CREATE EXTENSION IF NOT EXISTS pgrouting")
    ]
