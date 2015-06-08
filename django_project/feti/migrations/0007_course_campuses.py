# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('feti', '0006_auto_20150428_1532'),
    ]

    operations = [
        migrations.AddField(
            model_name='course',
            name='campuses',
            field=models.ManyToManyField(to='feti.Campus'),
            preserve_default=True,
        ),
    ]
