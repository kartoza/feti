# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('feti', '0007_course_campuses'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='course',
            name='campuses',
        ),
        migrations.AddField(
            model_name='campus',
            name='courses',
            field=models.ManyToManyField(to='feti.Course'),
            preserve_default=True,
        ),
    ]
