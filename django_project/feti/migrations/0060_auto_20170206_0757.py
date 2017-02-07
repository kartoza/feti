# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('feti', '0059_auto_20170206_0722'),
    ]

    operations = [
        migrations.AlterField(
            model_name='provider',
            name='icon',
            field=models.ImageField(null=True, blank=True, upload_to='icons/'),
        ),
    ]
