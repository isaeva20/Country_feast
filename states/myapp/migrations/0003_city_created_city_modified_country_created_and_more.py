# Generated by Django 5.0.3 on 2024-05-19 13:20

import myapp.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0002_alter_city_options_alter_country_options_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='city',
            name='created',
            field=models.DateTimeField(blank=True, default=myapp.models.get_datetime, null=True, validators=[myapp.models.check_created], verbose_name='created'),
        ),
        migrations.AddField(
            model_name='city',
            name='modified',
            field=models.DateTimeField(blank=True, default=myapp.models.get_datetime, null=True, validators=[myapp.models.check_modified], verbose_name='modified'),
        ),
        migrations.AddField(
            model_name='country',
            name='created',
            field=models.DateTimeField(blank=True, default=myapp.models.get_datetime, null=True, validators=[myapp.models.check_created], verbose_name='created'),
        ),
        migrations.AddField(
            model_name='country',
            name='modified',
            field=models.DateTimeField(blank=True, default=myapp.models.get_datetime, null=True, validators=[myapp.models.check_modified], verbose_name='modified'),
        ),
        migrations.AddField(
            model_name='feast',
            name='created',
            field=models.DateTimeField(blank=True, default=myapp.models.get_datetime, null=True, validators=[myapp.models.check_created], verbose_name='created'),
        ),
        migrations.AddField(
            model_name='feast',
            name='modified',
            field=models.DateTimeField(blank=True, default=myapp.models.get_datetime, null=True, validators=[myapp.models.check_modified], verbose_name='modified'),
        ),
    ]
