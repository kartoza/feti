# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('feti', '0027_auto_20150724_0534'),
    ]

    operations = [
        migrations.CreateModel(
            name='CampusCourseEntry',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True)),
                ('campus', models.ForeignKey(to='feti.Campus')),
                ('course', models.ForeignKey(to='feti.Course')),
            ],
            options={
                'managed': True,
            },
            bases=(models.Model,),
        ),
    ]
