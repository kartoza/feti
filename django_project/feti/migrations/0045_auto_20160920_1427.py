# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('feti', '0044_url'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='url',
            options={'ordering': ['date'], 'verbose_name': 'URL'},
        ),
        migrations.RenameField(
            model_name='url',
            old_name='random_words',
            new_name='random_string',
        ),
    ]
