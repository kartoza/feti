# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('feti', '0023_auto_20150602_1807'),
    ]

    operations = [
        migrations.AlterField(
            model_name='campus',
            name='_long_description',
            field=models.CharField(max_length=510, null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='course',
            name='_long_description',
            field=models.CharField(max_length=510, null=True, blank=True),
            preserve_default=True,
        ),
    ]
