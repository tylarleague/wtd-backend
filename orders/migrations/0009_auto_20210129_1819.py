# Generated by Django 3.1 on 2021-01-29 18:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0008_auto_20210129_1817'),
    ]

    operations = [
        migrations.AddField(
            model_name='historicalorder',
            name='approved_by_provider',
            field=models.BooleanField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='order',
            name='approved_by_provider',
            field=models.BooleanField(blank=True, null=True),
        ),
    ]
