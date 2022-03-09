# Generated by Django 3.1 on 2022-01-25 19:04

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0008_specialaccounts'),
        ('orders', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='City',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=2000)),
            ],
        ),
        migrations.CreateModel(
            name='Region',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=2000)),
                ('operator', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='operation_related_regions', to='accounts.operationprofile')),
            ],
        ),
        migrations.CreateModel(
            name='SpecialLocation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=2000)),
                ('one_way_price', models.IntegerField()),
                ('two_way_price', models.IntegerField()),
                ('city', models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='city_related_special_locations', to='orders.city')),
            ],
        ),
        migrations.CreateModel(
            name='SpecialLocationPoint',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=2000, null=True)),
                ('lat', models.FloatField()),
                ('lng', models.FloatField()),
                ('special_location', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='special_location_related_points', to='orders.speciallocation')),
            ],
        ),
        migrations.CreateModel(
            name='RegionPoint',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=2000, null=True)),
                ('lat', models.FloatField()),
                ('lng', models.FloatField()),
                ('region', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='region_related_points', to='orders.region')),
            ],
        ),
        migrations.CreateModel(
            name='CityPoint',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=2000, null=True)),
                ('lat', models.FloatField()),
                ('lng', models.FloatField()),
                ('city', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='city_related_points', to='orders.city')),
            ],
        ),
        migrations.AddField(
            model_name='city',
            name='region',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='region_related_cities', to='orders.region'),
        ),
        migrations.AddField(
            model_name='historicalorder',
            name='from_city',
            field=models.ForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to='orders.city'),
        ),
        migrations.AddField(
            model_name='historicalorder',
            name='from_region',
            field=models.ForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to='orders.region'),
        ),
        migrations.AddField(
            model_name='historicalorder',
            name='from_special_location',
            field=models.ForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to='orders.speciallocation'),
        ),
        migrations.AddField(
            model_name='historicalorder',
            name='to_city',
            field=models.ForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to='orders.city'),
        ),
        migrations.AddField(
            model_name='historicalorder',
            name='to_region',
            field=models.ForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to='orders.region'),
        ),
        migrations.AddField(
            model_name='historicalorder',
            name='to_special_location',
            field=models.ForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to='orders.speciallocation'),
        ),
        migrations.AddField(
            model_name='order',
            name='from_city',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='from_city_related_orders', to='orders.city'),
        ),
        migrations.AddField(
            model_name='order',
            name='from_region',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='from_region_related_orders', to='orders.region'),
        ),
        migrations.AddField(
            model_name='order',
            name='from_special_location',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='from_special_location_related_orders', to='orders.speciallocation'),
        ),
        migrations.AddField(
            model_name='order',
            name='to_city',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='to_city_related_orders', to='orders.city'),
        ),
        migrations.AddField(
            model_name='order',
            name='to_region',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='to_region_related_orders', to='orders.region'),
        ),
        migrations.AddField(
            model_name='order',
            name='to_special_location',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='to_special_location_related_orders', to='orders.speciallocation'),
        ),
    ]
