# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('feti', '0003_remove_provider_provider_address'),
    ]

    operations = [
        migrations.AlterField(
            model_name='provider',
            name='primary_institution',
            field=models.CharField(max_length=255),
        ),
    ]
