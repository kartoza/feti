# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django.contrib.gis.db.models.fields


class Migration(migrations.Migration):

    dependencies = [
        ('map_administrative', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Province',
            fields=[
                ('name', models.CharField(help_text='The name of the province or state.', max_length=50, verbose_name='')),
                ('polygon_geometry', django.contrib.gis.db.models.fields.MultiPolygonField(srid=4326)),
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('country', models.ForeignKey(to='map_administrative.Country')),
            ],
            options={
                'verbose_name_plural': 'Provinces',
            },
        ),
    ]
