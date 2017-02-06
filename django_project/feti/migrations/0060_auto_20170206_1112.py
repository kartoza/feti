# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import feti.models.url


class Migration(migrations.Migration):

    dependencies = [
        ('feti', '0059_auto_20170206_0722'),
    ]

    operations = [
        migrations.AlterField(
            model_name='url',
            name='random_string',
            field=models.CharField(unique=True, verbose_name='Random Words', max_length=255, default=feti.models.url.random_string),
        ),
    ]
