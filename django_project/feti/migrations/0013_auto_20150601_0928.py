# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('feti', '0012_auto_20150529_1148'),
    ]

    operations = [
        migrations.AlterField(
            model_name='educationtrainingqualityassurance',
            name='url',
            field=models.URLField(null=True, blank=True),
            preserve_default=True,
        ),
    ]
