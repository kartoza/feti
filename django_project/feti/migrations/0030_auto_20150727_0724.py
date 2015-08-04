# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.contrib.gis.db.models.fields


class Migration(migrations.Migration):

    dependencies = [
        ('feti', '0029_auto_20150727_0658'),
    ]

    operations = [
        migrations.AlterField(
            model_name='campus',
            name='location',
            field=django.contrib.gis.db.models.fields.PointField(default=b'POINT(28.034088 -26.195246)', srid=4326, null=True, blank=True),
            preserve_default=True,
        ),
    ]
