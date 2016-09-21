# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('feti', '0043_auto_20160919_0515'),
    ]

    operations = [
        migrations.CreateModel(
            name='URL',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('random_words', models.CharField(verbose_name='Random Words', max_length=255)),
                ('url', models.URLField(verbose_name='Url', max_length=1000)),
                ('date', models.DateField(verbose_name='Date', default=datetime.date.today)),
            ],
            options={
                'verbose_name': 'URLs',
                'ordering': ['date'],
            },
        ),
    ]
