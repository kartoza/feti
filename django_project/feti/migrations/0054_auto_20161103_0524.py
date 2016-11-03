# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('feti', '0053_campuscoursesfavorite_user'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='stepdetail',
            name='course',
        ),
        migrations.AddField(
            model_name='stepdetail',
            name='course',
            field=models.ManyToManyField(null=True, blank=True, to='feti.Course'),
        ),
    ]
