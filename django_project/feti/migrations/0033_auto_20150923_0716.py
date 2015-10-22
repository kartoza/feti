# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('feti', '0032_auto_20150909_1127'),
    ]

    operations = [
        migrations.AlterField(
            model_name='campus',
            name='_campus_popup',
            field=models.CharField(max_length=1020, null=True, blank=True),
        ),
    ]
