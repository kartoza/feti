# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('map_administrative', '0002_province'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='country',
            options={'ordering': ['name'], 'verbose_name_plural': 'Countries'},
        ),
        migrations.AlterModelOptions(
            name='province',
            options={'ordering': ['name'], 'verbose_name_plural': 'Provinces'},
        ),
    ]
