# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('feti', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='nationalcertificatevocational',
            name='national_certificate_vocational_description',
            field=models.CharField(max_length=255, null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='nationalqualificationsframework',
            name='description',
            field=models.CharField(max_length=255),
            preserve_default=True,
        ),
    ]
