# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('feti', '0038_auto_20160830_0443'),
    ]

    operations = [
        migrations.AlterField(
            model_name='campusofficial',
            name='campus',
            field=models.ManyToManyField(verbose_name='Providers', to='feti.Campus'),
        ),
    ]
