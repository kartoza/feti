# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('feti', '0019_auto_20150601_1255'),
    ]

    operations = [
        migrations.AlterField(
            model_name='nationalqualificationsframework',
            name='link',
            field=models.URLField(null=True, blank=True),
            preserve_default=True,
        ),
    ]
