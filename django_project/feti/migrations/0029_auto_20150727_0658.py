# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.core.validators


class Migration(migrations.Migration):

    dependencies = [
        ('feti', '0028_campuscourseentry'),
    ]

    operations = [
        migrations.AlterField(
            model_name='address',
            name='phone',
            field=models.CharField(blank=True, max_length=100, null=True, validators=[django.core.validators.RegexValidator(regex='^\\+?(\\d)+(\\d(-)?)*(\\d)+$', message=b"Phone number should have the following format: '+27888888888 or 021-777-777'.")]),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='campus',
            name='address',
            field=models.ForeignKey(blank=True, to='feti.Address', null=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='provider',
            name='website',
            field=models.URLField(null=True, blank=True),
            preserve_default=True,
        ),
    ]
