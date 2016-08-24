# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings
import django.core.validators


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('feti', '0034_auto_20160617_0628'),
    ]

    operations = [
        migrations.CreateModel(
            name='CampusOfficial',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('department', models.CharField(max_length=100)),
                ('phone', models.CharField(blank=True, max_length=15, validators=[django.core.validators.RegexValidator(regex='^\\+?1?\\d{9,15}$', message=b"Phone number must be entered in the format: '+6288888888888'. Up to 15 digits allowed.")])),
                ('campus', models.OneToOneField(related_name='official_provider', null=True, blank=True, to='feti.Campus')),
                ('user', models.OneToOneField(to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
