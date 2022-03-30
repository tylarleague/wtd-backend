# Generated by Django 3.1 on 2021-01-09 14:28

from django.conf import settings
import django.contrib.postgres.fields.jsonb
from django.db import migrations, models
import django.db.models.deletion
import simple_history.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('from_location', django.contrib.postgres.fields.jsonb.JSONField(blank=True, null=True)),
                ('to_location', django.contrib.postgres.fields.jsonb.JSONField(blank=True, null=True)),
                ('order_date', models.DateField(blank=True, null=True)),
                ('arrival_time', models.TimeField(blank=True, null=True)),
                ('status', models.CharField(default='open', max_length=50)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='owner_related_orders', to='accounts.clientprofile')),
                ('patient', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='patient_related_orders', to='accounts.person')),
                ('appointment_approval', models.FileField(blank=True, null=True, upload_to='appointment_approvals')),
                ('approved_by_client', models.BooleanField(default=False)),
                ('approved_by_provider', models.BooleanField(blank=True, null=True)),
                ('health_institution', models.BooleanField(default=False)),
                ('notes', models.CharField(blank=True, max_length=500, null=True)),
                ('order_type', models.CharField(default='ONE_WAY', max_length=50)),
                ('payment_authorized', models.BooleanField(default=False)),
                ('provider', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='provider_related_orders', to='accounts.providerprofile')),
                ('waiting_time', models.IntegerField(blank=True, null=True))
            ],
        ),
        migrations.CreateModel(
            name='HistoricalOrder',
            fields=[
                ('id', models.IntegerField(auto_created=True, blank=True, db_index=True, verbose_name='ID')),
                ('from_location', django.contrib.postgres.fields.jsonb.JSONField(blank=True, null=True)),
                ('to_location', django.contrib.postgres.fields.jsonb.JSONField(blank=True, null=True)),
                ('order_date', models.DateField(blank=True, null=True)),
                ('arrival_time', models.TimeField(blank=True, null=True)),
                ('status', models.CharField(default='open', max_length=50)),
                ('created_at', models.DateTimeField(blank=True, editable=False)),
                ('history_id', models.AutoField(primary_key=True, serialize=False)),
                ('history_date', models.DateTimeField()),
                ('history_change_reason', models.CharField(max_length=100, null=True)),
                ('history_type', models.CharField(choices=[('+', 'Created'), ('~', 'Changed'), ('-', 'Deleted')], max_length=1)),
                ('history_user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to=settings.AUTH_USER_MODEL)),
                ('owner', models.ForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to='accounts.clientprofile')),
                ('patient', models.ForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to='accounts.person')),
                ('appointment_approval',models.TextField(blank=True, max_length=100, null=True)),
                ('approved_by_client', models.BooleanField(default=False)),
                ('approved_by_provider',models.BooleanField(blank=True, null=True)),
                ('health_institution', models.BooleanField(default=False)),
                ('notes', models.CharField(blank=True, max_length=500, null=True)),
                ('order_type', models.CharField(default='ONE_WAY', max_length=50)),
                ('payment_authorized', models.BooleanField(default=False)),
                ('provider', models.ForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to='accounts.providerprofile')),
                ('waiting_time', models.IntegerField(blank=True, null=True))
            ],
            options={
                'verbose_name': 'historical order',
                'ordering': ('-history_date', '-history_id'),
                'get_latest_by': 'history_date',
            },
            bases=(simple_history.models.HistoricalChanges, models.Model),
        ),
        migrations.CreateModel(
            name='ExtraServices',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('service_name', models.CharField(max_length=100)),
                ('service_cost', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='Invoice',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('distance_value', models.IntegerField()),
                ('distance_text', models.CharField(max_length=50)),
                ('duration_value', models.IntegerField()),
                ('duration_text', models.CharField(max_length=50)),
                ('cost', models.IntegerField()),
                ('initial_cost', models.IntegerField(default=0)),
                ('order', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='order_related_invoice', to='orders.order')),
            ],
        ),
        migrations.CreateModel(
            name='AmbReport',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('history', models.CharField(blank=True, max_length=2000, null=True)),
                ('temp', models.CharField(blank=True, max_length=100, null=True)),
                ('oxygen', models.CharField(blank=True, max_length=100, null=True)),
                ('BP', models.CharField(blank=True, max_length=100, null=True)),
                ('pulse', models.CharField(blank=True, max_length=100, null=True)),
                ('infectious_diseases', models.BooleanField(default=False)),
                ('order', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='order_related_report', to='orders.order')),
            ],
        ),
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
                ('special_price', models.IntegerField(default=0)),
                ('city', models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='city_related_special_locations', to='orders.city')),
            ],
        ),
        migrations.AddField(
            model_name='historicalorder',
            name='discharge_approval',
            field=models.TextField(blank=True, max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='historicalorder',
            name='is_contagious',
            field=models.BooleanField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='historicalorder',
            name='is_discharged',
            field=models.BooleanField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='historicalorder',
            name='is_emergency',
            field=models.BooleanField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='historicalorder',
            name='is_overweight',
            field=models.BooleanField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='historicalorder',
            name='needs_oxygen',
            field=models.BooleanField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='historicalorder',
            name='operator',
            field=models.ForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to='accounts.operationprofile'),
        ),
        migrations.AddField(
            model_name='historicalorder',
            name='order_block_end',
            field=models.TimeField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='historicalorder',
            name='order_block_start',
            field=models.TimeField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='historicalorder',
            name='send_sms',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='order',
            name='discharge_approval',
            field=models.FileField(blank=True, null=True, upload_to='discharge_approvals'),
        ),
        migrations.AddField(
            model_name='order',
            name='is_contagious',
            field=models.BooleanField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='order',
            name='is_discharged',
            field=models.BooleanField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='order',
            name='is_emergency',
            field=models.BooleanField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='order',
            name='is_overweight',
            field=models.BooleanField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='order',
            name='needs_oxygen',
            field=models.BooleanField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='order',
            name='operator',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='operator_related_orders', to='accounts.operationprofile'),
        ),
        migrations.AddField(
            model_name='order',
            name='order_block_end',
            field=models.TimeField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='order',
            name='order_block_start',
            field=models.TimeField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='order',
            name='send_sms',
            field=models.BooleanField(default=True),
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
            name='OrderPossibleProvider',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('importance', models.FloatField()),
                ('order_block_start', models.TimeField(blank=True, null=True)),
                ('order_block_end', models.TimeField(blank=True, null=True)),
                ('order', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='order_possible_providers', to='orders.order')),
                ('provider', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='provider_possible_orders', to='accounts.providerprofile')),
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
