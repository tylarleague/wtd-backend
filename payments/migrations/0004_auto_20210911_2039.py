# Generated by Django 3.1 on 2021-09-11 20:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('payments', '0003_auto_20210911_2036'),
    ]

    operations = [
        migrations.AlterField(
            model_name='payment',
            name='status',
            field=models.CharField(blank=True, max_length=500, null=True),
        ),
        migrations.AlterField(
            model_name='payment',
            name='tap_charge_id',
            field=models.CharField(blank=True, max_length=500, null=True),
        ),
    ]