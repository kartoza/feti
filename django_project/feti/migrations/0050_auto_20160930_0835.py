# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('feti', '0049_auto_20160928_1051'),
    ]

    operations = [
        migrations.AlterField(
            model_name='fieldofstudy',
            name='field_of_study_description',
            field=models.CharField(null=True, max_length=150, blank=True),
        ),
    ]
