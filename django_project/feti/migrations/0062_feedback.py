# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('feti', '0061_merge'),
    ]

    operations = [
        migrations.CreateModel(
            name='Feedback',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('title', models.CharField(verbose_name='Title', max_length=250)),
                ('name', models.CharField(verbose_name='Name', max_length=200)),
                ('contact', models.CharField(verbose_name='Contact', max_length=200)),
                ('comments', models.TextField(verbose_name='Comments', max_length=500)),
                ('read', models.BooleanField(help_text='Feedback is read/processed', default=False, verbose_name='Read')),
                ('date', models.DateField(verbose_name='Date', default=datetime.date.today)),
            ],
            options={
                'ordering': ['title'],
            },
        ),
    ]
