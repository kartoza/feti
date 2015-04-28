# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('feti', '0002_auto_20150424_1300'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='provider',
            name='provider_address',
        ),
    ]
