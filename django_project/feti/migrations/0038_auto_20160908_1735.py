# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('feti', '0037_auto_20160823_1120'),
    ]

    operations = [
        migrations.CreateModel(
            name='LearningPathway',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True)),
                ('pathway_number', models.IntegerField()),
            ],
            options={
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='Occupation',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True)),
                ('occupation', models.CharField(max_length=150)),
                ('green_occupation', models.BooleanField(default=False)),
                ('green_skill', models.BooleanField(default=False)),
                ('description', models.CharField(max_length=500)),
                ('tasks', models.TextField(blank=True, null=True)),
                ('occupation_regulation', models.TextField(blank=True, null=True)),
                ('learning_pathway_description', models.TextField(blank=True, null=True)),
                ('learning_pathways', models.ManyToManyField(to='feti.LearningPathway')),
            ],
            options={
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='Step',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, primary_key=True, verbose_name='ID')),
                ('step_number', models.IntegerField()),
                ('title', models.CharField(blank=True, null=True, max_length=255)),
                ('detail', models.CharField(blank=True, null=True, max_length=510)),
                ('course', models.ForeignKey(to='feti.Course')),
            ],
            options={
                'managed': True,
            },
        ),
        migrations.AddField(
            model_name='learningpathway',
            name='steps',
            field=models.ManyToManyField(to='feti.Step'),
        ),
    ]
