# Generated by Django 5.0.6 on 2024-09-01 11:15

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('storehouse', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='storehouserecord',
            name='date',
            field=models.DateField(default=django.utils.timezone.now),
        ),
    ]
