# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.core.validators


class Migration(migrations.Migration):

    dependencies = [
        ('feti', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Address',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('address_line_1', models.CharField(max_length=100)),
                ('address_line_2', models.CharField(max_length=100)),
                ('address_line_3', models.CharField(max_length=100)),
                ('town', models.CharField(max_length=100)),
                ('postal_code', models.CharField(max_length=4, validators=[django.core.validators.RegexValidator(regex=b'^\\d{4,4}$', message=b'Postal code consists of 4 digits.')])),
                ('phone', models.CharField(blank=True, max_length=12, null=True, validators=[django.core.validators.RegexValidator(regex=b'^\\+\\d{12,12}$', message=b"Phone number should have the following format: '+27888888888'.")])),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Provider',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True)),
                ('primary_institution', models.CharField(max_length=100)),
                ('website', models.URLField()),
                ('status', models.BooleanField(default=True)),
                ('provider_address', models.ForeignKey(to='feti.Address')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
