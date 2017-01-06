# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django.contrib.gis.db.models.fields


class Migration(migrations.Migration):

    dependencies = [
        ('map_administrative', '0005_district'),
    ]

    operations = [
        migrations.CreateModel(
            name='Municipality',
            fields=[
                ('name', models.CharField(verbose_name='', help_text='The name of municipality.', max_length=50)),
                ('polygon_geometry', django.contrib.gis.db.models.fields.MultiPolygonField(srid=4326)),
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('district', models.ForeignKey(to='map_administrative.District')),
            ],
            options={
                'verbose_name_plural': 'Municipalities',
                'ordering': ['name'],
            },
        ),
    ]
