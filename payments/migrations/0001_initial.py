# Generated by Django 3.1 on 2022-01-24 16:07

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('orders', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Payment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tap_id', models.CharField(max_length=500)),
                ('tap_refund_id', models.CharField(blank=True, max_length=500, null=True)),
                ('status', models.CharField(blank=True, max_length=500, null=True)),
                ('order', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='order_related_payments', to='orders.order')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user_related_payments', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
