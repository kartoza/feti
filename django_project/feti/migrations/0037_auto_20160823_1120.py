# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django.core.validators


class Migration(migrations.Migration):

    dependencies = [
        ('feti', '0036_auto_20160812_0501'),
    ]

    operations = [
        migrations.AlterField(
            model_name='address',
            name='phone',
            field=models.CharField(max_length=100, blank=True, null=True, validators=[django.core.validators.RegexValidator(message="Phone number should have the following format: '+27888888888 or 021-777-777'.", regex='^\\+?(\\d)+(\\d(-)?)*(\\d)+$')]),
        ),
        migrations.AlterField(
            model_name='campusofficial',
            name='phone',
            field=models.CharField(max_length=15, blank=True, validators=[django.core.validators.RegexValidator(message="Phone number must be entered in the format: '+6288888888888'. Up to 15 digits allowed.", regex='^\\+?1?\\d{9,15}$')]),
        ),
    ]
