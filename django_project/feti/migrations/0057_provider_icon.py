# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('feti', '0056_auto_20161104_1255'),
    ]

    operations = [
        migrations.AddField(
            model_name='provider',
            name='icon',
            field=models.ImageField(null=True, blank=True, upload_to='/home/web/media/icons/'),
        ),
    ]
