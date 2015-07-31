# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('feti', '0026_auto_20150716_0049'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='address',
            options={'verbose_name_plural': 'Addreses'},
        ),
        migrations.AddField(
            model_name='address',
            name='campus_fk',
            field=models.OneToOneField(related_name='address_fk', null=True, to='feti.Campus'),
            preserve_default=True,
        ),
    ]
