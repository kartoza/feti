# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('feti', '0002_address_provider'),
    ]

    operations = [
        migrations.AddField(
            model_name='campus',
            name='address',
            field=models.ForeignKey(default=1, to='feti.Address'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='campus',
            name='provider',
            field=models.ForeignKey(default=1, to='feti.Provider'),
            preserve_default=False,
        ),
    ]
