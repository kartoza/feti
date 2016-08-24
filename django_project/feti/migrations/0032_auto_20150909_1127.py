# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('feti', '0031_auto_20150806_1558'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='campus',
            options={'ordering': ['campus'], 'verbose_name': 'Provider'},
        ),
        migrations.AlterModelOptions(
            name='provider',
            options={'ordering': ['primary_institution'], 'verbose_name': 'Primary institution'},
        ),
        migrations.AlterField(
            model_name='campus',
            name='campus',
            field=models.CharField(max_length=150, null=True, verbose_name='Provider', blank=True),
        ),
        migrations.AlterField(
            model_name='provider',
            name='primary_institution',
            field=models.CharField(max_length=255, null=True, verbose_name='Primary institution', blank=True),
        ),
    ]
