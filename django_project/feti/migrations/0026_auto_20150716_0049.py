# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('feti', '0025_campus__complete'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='address',
            options={'verbose_name_plural': 'Addresses'},
        ),
        migrations.AlterModelOptions(
            name='campus',
            options={'verbose_name_plural': 'Campuses'},
        ),
        migrations.AddField(
            model_name='campus',
            name='_campus_popup',
            field=models.CharField(max_length=510, null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='course',
            name='_course_popup',
            field=models.CharField(max_length=510, null=True, blank=True),
            preserve_default=True,
        ),
    ]
