# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('feti', '0044_auto_20160919_0330'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='stepdetail',
            options={'verbose_name_plural': 'steps', 'verbose_name': 'step', 'managed': True},
        ),
    ]
