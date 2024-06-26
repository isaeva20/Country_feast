# Generated by Django 5.0.3 on 2024-06-09 17:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0006_alter_city_country_alter_feast_countries'),
    ]

    operations = [
        migrations.AlterField(
            model_name='feast',
            name='countries',
            field=models.ManyToManyField(through='myapp.CountryToFeast', to='myapp.country', verbose_name='countries'),
        ),
    ]
