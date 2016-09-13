# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('feti', '0037_auto_20160823_1120'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='campusofficial',
            name='campus',
        ),
        migrations.AddField(
            model_name='campusofficial',
            name='campus',
            field=models.ManyToManyField(to='feti.Campus'),
        ),
    ]
