# Generated by Django 5.0.7 on 2024-08-29 15:51

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('YorkEats', '0002_place_is_open'),
    ]

    operations = [
        migrations.AddField(
            model_name='place',
            name='timestamp',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
    ]
