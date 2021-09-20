# Generated by Django 3.1 on 2021-09-06 08:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0016_ambreport'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ambreport',
            name='BP',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='ambreport',
            name='history',
            field=models.CharField(blank=True, max_length=2000, null=True),
        ),
        migrations.AlterField(
            model_name='ambreport',
            name='oxygen',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='ambreport',
            name='pulse',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='ambreport',
            name='temp',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]