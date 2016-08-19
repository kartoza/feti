# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('feti', '0035_campusofficial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='campusofficial',
            options={'verbose_name': 'Provider Official'},
        ),
    ]
