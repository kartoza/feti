# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('feti', '0048_auto_20160926_1001'),
    ]

    operations = [
        migrations.AlterField(
            model_name='occupation',
            name='description',
            field=models.TextField(blank=True, null=True),
        ),
    ]
