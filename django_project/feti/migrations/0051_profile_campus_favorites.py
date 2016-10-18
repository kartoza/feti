# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('feti', '0050_auto_20160930_0835'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='campus_favorites',
            field=models.ManyToManyField(to='feti.Campus'),
        ),
    ]
