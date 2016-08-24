# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.core.validators


class Migration(migrations.Migration):

    dependencies = [
        ('feti', '0008_auto_20150518_1153'),
    ]

    operations = [
        migrations.AlterField(
            model_name='address',
            name='address_line_1',
            field=models.CharField(max_length=100, null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='address',
            name='address_line_2',
            field=models.CharField(max_length=100, null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='address',
            name='address_line_3',
            field=models.CharField(max_length=100, null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='address',
            name='postal_code',
            field=models.CharField(blank=True, max_length=4, null=True, validators=[django.core.validators.RegexValidator(regex='^\\d{4,4}$', message='Postal code consists of 4 digits.')]),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='address',
            name='town',
            field=models.CharField(max_length=100, null=True, blank=True),
            preserve_default=True,
        ),
    ]
