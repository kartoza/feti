# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('feti', '0030_auto_20150727_0724'),
    ]

    operations = [
        migrations.AlterField(
            model_name='campus',
            name='provider',
            field=models.ForeignKey(related_name='campuses', to='feti.Provider'),
        ),
    ]
