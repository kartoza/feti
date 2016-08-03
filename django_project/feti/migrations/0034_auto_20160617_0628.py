# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('feti', '0033_auto_20150923_0716'),
    ]

    operations = [
        migrations.AlterField(
            model_name='course',
            name='national_learners_records_database',
            field=models.CharField(help_text=b'National Learners` Records Database (NLRD)', max_length=50, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='provider',
            name='status',
            field=models.BooleanField(default=True, verbose_name=b'Public primary institution'),
        ),
    ]
