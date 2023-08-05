# Generated by Django 2.0.13 on 2019-06-13 13:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('geostore', '0025_auto_20190613_1341'),
    ]

    operations = [
        migrations.AddIndex(
            model_name='feature',
            index=models.Index(fields=['updated_at', 'layer'], name='geo_featu_updated_cfeac3_idx'),
        ),
    ]
