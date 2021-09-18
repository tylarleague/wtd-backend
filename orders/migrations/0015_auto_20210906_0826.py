# Generated by Django 3.1 on 2021-09-06 08:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0014_auto_20210708_1200'),
    ]

    operations = [
        migrations.AddField(
            model_name='historicalorder',
            name='appointment_approval',
            field=models.TextField(blank=True, max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='historicalorder',
            name='health_institution',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='order',
            name='appointment_approval',
            field=models.FileField(blank=True, null=True, upload_to='appointment_approvals'),
        ),
        migrations.AddField(
            model_name='order',
            name='health_institution',
            field=models.BooleanField(default=False),
        ),
    ]
