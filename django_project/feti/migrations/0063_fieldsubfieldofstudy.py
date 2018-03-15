# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('feti', '0062_feedback'),
    ]

    operations = [
        migrations.CreateModel(
            name='FieldSubfieldOfStudy',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True)),
                ('field_of_study', models.ForeignKey(to='feti.FieldOfStudy')),
                ('subfield_of_study', models.ManyToManyField(to='feti.SubFieldOfStudy')),
            ],
            options={
                'managed': True,
            },
        ),
    ]
