# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('feti', '0051_profile_campus_favorites'),
    ]

    operations = [
        migrations.CreateModel(
            name='CampusCoursesFavorite',
            fields=[
                ('id', models.AutoField(auto_created=True, serialize=False, verbose_name='ID', primary_key=True)),
                ('campus', models.ForeignKey(to='feti.Campus')),
                ('courses', models.ManyToManyField(to='feti.Course')),
            ],
        ),
        migrations.RemoveField(
            model_name='profile',
            name='campus_favorites',
        ),
    ]
