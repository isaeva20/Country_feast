# Generated by Django 5.0.3 on 2024-06-09 19:06

import myapp.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0009_alter_country_area_country'),
    ]

    operations = [
        migrations.AlterField(
            model_name='country',
            name='population',
            field=models.PositiveIntegerField(blank=True, null=True, validators=[myapp.models.check_positive], verbose_name='population'),
        ),
    ]