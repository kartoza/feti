# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.core.validators


class Migration(migrations.Migration):

    dependencies = [
        ('feti', '0021_auto_20150601_1327'),
    ]

    operations = [
        migrations.AlterField(
            model_name='course',
            name='national_learners_records_database',
            field=models.CharField(blank=True, max_length=50, null=True, help_text=b'National Learners` Records Database (NLRD)', validators=[django.core.validators.RegexValidator(regex=b'^\\d{15,15}$', message=b"National Learners Records Database: '123456789012345'.")]),
            preserve_default=True,
        ),
    ]
