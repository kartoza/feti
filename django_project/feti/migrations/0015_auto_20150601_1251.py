# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('feti', '0014_auto_20150601_1250'),
    ]

    operations = [
        migrations.AlterField(
            model_name='course',
            name='field_of_study',
            field=models.ForeignKey(blank=True, to='feti.FieldOfStudy', null=True),
            preserve_default=True,
        ),
    ]
