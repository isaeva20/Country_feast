# Generated by Django 5.0.3 on 2024-05-19 14:16

import myapp.models
import uuid
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0003_city_created_city_modified_country_created_and_more'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='countrytofeast',
            options={'verbose_name': 'Relationship country feast', 'verbose_name_plural': 'Relationships country feast'},
        ),
        migrations.AddField(
            model_name='countrytofeast',
            name='created',
            field=models.DateTimeField(blank=True, default=myapp.models.get_datetime, null=True, validators=[myapp.models.check_created], verbose_name='created'),
        ),
        migrations.AlterField(
            model_name='city',
            name='area_city',
            field=models.PositiveIntegerField(blank=True, null=True, verbose_name='area city'),
        ),
        migrations.AlterField(
            model_name='city',
            name='coordinates',
            field=models.TextField(blank=True, null=True, verbose_name='coordinates'),
        ),
        migrations.AlterField(
            model_name='city',
            name='name',
            field=models.TextField(verbose_name='name'),
        ),
        migrations.AlterField(
            model_name='city',
            name='population',
            field=models.PositiveIntegerField(blank=True, null=True, verbose_name='population'),
        ),
        migrations.AlterField(
            model_name='country',
            name='area_country',
            field=models.PositiveIntegerField(verbose_name='area country'),
        ),
        migrations.AlterField(
            model_name='country',
            name='hymn',
            field=models.TextField(blank=True, null=True, verbose_name='hymn'),
        ),
        migrations.AlterField(
            model_name='country',
            name='name',
            field=models.TextField(verbose_name='name'),
        ),
        migrations.AlterField(
            model_name='country',
            name='population',
            field=models.PositiveIntegerField(blank=True, null=True, verbose_name='population'),
        ),
        migrations.AlterField(
            model_name='countrytofeast',
            name='id',
            field=models.UUIDField(blank=True, default=uuid.uuid4, editable=False, primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='feast',
            name='countries',
            field=models.ManyToManyField(through='myapp.CountryToFeast', to='myapp.country', verbose_name='countries'),
        ),
        migrations.AlterField(
            model_name='feast',
            name='date_of_feast',
            field=models.DateField(blank=True, null=True, verbose_name='date of feast'),
        ),
        migrations.AlterField(
            model_name='feast',
            name='description',
            field=models.TextField(blank=True, null=True, verbose_name='description'),
        ),
        migrations.AlterField(
            model_name='feast',
            name='title',
            field=models.TextField(verbose_name='title'),
        ),
    ]