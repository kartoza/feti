# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('feti', '0039_auto_20160830_1102'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='campusofficial',
            name='department',
        ),
        migrations.RemoveField(
            model_name='campusofficial',
            name='phone',
        ),
    ]
