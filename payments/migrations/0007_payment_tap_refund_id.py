# Generated by Django 3.1 on 2021-09-20 19:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('payments', '0006_auto_20210920_1722'),
    ]

    operations = [
        migrations.AddField(
            model_name='payment',
            name='tap_refund_id',
            field=models.CharField(blank=True, max_length=500, null=True),
        ),
    ]
