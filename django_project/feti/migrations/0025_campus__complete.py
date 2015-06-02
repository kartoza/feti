# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('feti', '0024_auto_20150602_1811'),
    ]

    operations = [
        migrations.AddField(
            model_name='campus',
            name='_complete',
            field=models.BooleanField(default=True),
            preserve_default=True,
        ),
    ]
