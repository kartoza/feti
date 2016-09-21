# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('feti', '0042_merge'),
    ]

    operations = [
        migrations.AlterField(
            model_name='step',
            name='course',
            field=models.ForeignKey(null=True, blank=True, to='feti.Course'),
        ),
    ]
