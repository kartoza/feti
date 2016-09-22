# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django.contrib.gis.db.models.fields


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Country',
            fields=[
                ('name', models.CharField(help_text='The name of the country.', max_length=50, verbose_name='')),
                ('polygon_geometry', django.contrib.gis.db.models.fields.MultiPolygonField(srid=4326)),
                ('id', models.AutoField(serialize=False, primary_key=True)),
            ],
            options={
                'verbose_name_plural': 'Countries',
            },
        ),
    ]
