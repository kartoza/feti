# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django.contrib.gis.db.models.fields


class Migration(migrations.Migration):

    dependencies = [
        ('map_administrative', '0004_auto_20160923_0638'),
    ]

    operations = [
        migrations.CreateModel(
            name='District',
            fields=[
                ('name', models.CharField(verbose_name='', max_length=50, help_text='The name of district.')),
                ('polygon_geometry', django.contrib.gis.db.models.fields.MultiPolygonField(srid=4326)),
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('province', models.ForeignKey(to='map_administrative.Province')),
            ],
            options={
                'verbose_name_plural': 'Districts',
                'ordering': ['name'],
            },
        ),
    ]
