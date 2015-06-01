# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('feti', '0009_auto_20150529_1102'),
    ]

    operations = [
        migrations.AlterField(
            model_name='provider',
            name='primary_institution',
            field=models.CharField(max_length=255, null=True, blank=True),
            preserve_default=True,
        ),
    ]
