# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.core.validators


class Migration(migrations.Migration):

    dependencies = [
        ('feti', '0004_auto_20150428_1412'),
    ]

    operations = [
        migrations.AlterField(
            model_name='address',
            name='phone',
            field=models.CharField(blank=True, max_length=40, null=True, validators=[django.core.validators.RegexValidator(regex=b'^\\+\\d{12,12}$', message=b"Phone number should have the following format: '+27888888888'.")]),
        ),
    ]
