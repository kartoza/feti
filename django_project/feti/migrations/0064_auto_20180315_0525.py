# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('feti', '0063_fieldsubfieldofstudy'),
    ]

    operations = [
        migrations.AlterField(
            model_name='address',
            name='campus_fk',
            field=models.OneToOneField(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='address_fk', to='feti.Campus'),
        ),
    ]
