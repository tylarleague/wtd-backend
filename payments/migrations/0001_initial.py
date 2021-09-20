# Generated by Django 3.1 on 2021-09-11 12:30

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('orders', '0017_auto_20210906_0846'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='TapToken',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tap_token_id', models.CharField(max_length=500)),
                ('order', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='order_related_tokens', to='orders.order')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='owner_related_tokens', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]