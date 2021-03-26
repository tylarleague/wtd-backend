# Generated by Django 3.1 on 2021-01-24 12:04

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0004_auto_20210124_1034'),
    ]

    operations = [
        migrations.CreateModel(
            name='ExtraServices',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('service_name', models.CharField(max_length=100)),
                ('service_cost', models.IntegerField()),
                ('order', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='ordr_extra_services', to='orders.order')),
            ],
        ),
    ]
