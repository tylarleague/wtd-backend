# Generated by Django 3.1 on 2022-03-29 14:53

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
       migrations.AddField(
            model_name='organization',
            name='lng',
            field=models.FloatField(blank=True, null=True),
        ),
    ]
