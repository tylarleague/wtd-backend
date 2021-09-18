# Generated by Django 3.1 on 2021-09-06 08:39

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0015_auto_20210906_0826'),
    ]

    operations = [
        migrations.CreateModel(
            name='AmbReport',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('history', models.CharField(max_length=2000)),
                ('temp', models.CharField(max_length=100)),
                ('oxygen', models.CharField(max_length=100)),
                ('BP', models.CharField(max_length=100)),
                ('pulse', models.CharField(max_length=100)),
                ('infectious_diseases', models.BooleanField(default=False)),
                ('order', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='order_related_report', to='orders.order')),
            ],
        ),
    ]
