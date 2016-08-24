# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.core.validators


class Migration(migrations.Migration):

    dependencies = [
        ('feti', '0013_auto_20150601_0928'),
    ]

    operations = [
        migrations.AlterField(
            model_name='course',
            name='national_learners_records_database',
            field=models.CharField(blank=True, max_length=15, null=True, help_text='National Learners` Records Database (NLRD)', validators=[django.core.validators.RegexValidator(regex='^\\d{15,15}$', message=b"National Learners Records Database: '123456789012345'.")]),
            preserve_default=True,
        ),
    ]
