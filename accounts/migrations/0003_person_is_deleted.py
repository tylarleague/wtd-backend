# Generated by Django 3.1 on 2022-10-15 15:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0002_auto_20220329_1453'),
    ]

    operations = [
        migrations.AddField(
            model_name='person',
            name='is_deleted',
            field=models.BooleanField(default=False),
        ),
    ]
