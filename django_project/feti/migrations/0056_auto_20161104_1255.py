# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('feti', '0055_auto_20161104_0557'),
    ]

    operations = [
        migrations.AlterField(
            model_name='course',
            name='registration_status',
            field=models.CharField(max_length=100, null=True, blank=True),
        ),
    ]
