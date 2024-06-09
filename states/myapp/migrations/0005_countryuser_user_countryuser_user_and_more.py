# Generated by Django 5.0.3 on 2024-05-27 17:49

import django.db.models.deletion
import myapp.models
import uuid
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
        ('myapp', '0004_alter_countrytofeast_options_countrytofeast_created_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='CountryUser',
            fields=[
                ('id', models.UUIDField(blank=True, default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('created', models.DateTimeField(blank=True, default=myapp.models.get_datetime, null=True, validators=[myapp.models.check_created], verbose_name='created')),
                ('country', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='myapp.country', verbose_name='country')),
            ],
            options={
                'verbose_name': 'relationship country user',
                'verbose_name_plural': 'relationships country user',
                'db_table': '"states"."country_user"',
            },
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('created', models.DateTimeField(blank=True, default=myapp.models.get_datetime, null=True, validators=[myapp.models.check_created], verbose_name='created')),
                ('modified', models.DateTimeField(blank=True, default=myapp.models.get_datetime, null=True, validators=[myapp.models.check_modified], verbose_name='modified')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to=settings.AUTH_USER_MODEL)),
                ('countries', models.ManyToManyField(through='myapp.CountryUser', to='myapp.country', verbose_name='countries')),
            ],
            options={
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
                'db_table': '"states"."user"',
            },
        ),
        migrations.AddField(
            model_name='countryuser',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='myapp.user', verbose_name='user'),
        ),
        migrations.AlterUniqueTogether(
            name='countryuser',
            unique_together={('country', 'user')},
        ),
    ]
