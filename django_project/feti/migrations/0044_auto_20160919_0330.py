# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('feti', '0043_auto_20160916_1113'),
    ]

    operations = [
        migrations.AlterField(
            model_name='stepdetail',
            name='detail',
            field=models.CharField(max_length=1024, null=True, blank=True),
        ),
    ]
