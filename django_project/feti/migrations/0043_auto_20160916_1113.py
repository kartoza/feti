# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('feti', '0042_merge'),
    ]

    operations = [
        migrations.CreateModel(
            name='StepDetail',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('title', models.CharField(blank=True, null=True, max_length=255)),
                ('detail', models.CharField(blank=True, null=True, max_length=510)),
                ('course', models.ForeignKey(to='feti.Course', blank=True, null=True)),
            ],
            options={
                'managed': True,
            },
        ),
        migrations.RenameField(
            model_name='occupation',
            old_name='green_skill',
            new_name='scarce_skill',
        ),
        migrations.RemoveField(
            model_name='learningpathway',
            name='steps',
        ),
        migrations.RemoveField(
            model_name='occupation',
            name='learning_pathways',
        ),
        migrations.RemoveField(
            model_name='step',
            name='course',
        ),
        migrations.RemoveField(
            model_name='step',
            name='detail',
        ),
        migrations.RemoveField(
            model_name='step',
            name='title',
        ),
        migrations.AddField(
            model_name='learningpathway',
            name='occupation',
            field=models.ForeignKey(to='feti.Occupation', default=None),
        ),
        migrations.AddField(
            model_name='step',
            name='learning_pathway',
            field=models.ForeignKey(to='feti.LearningPathway', default=None),
        ),
        migrations.AlterField(
            model_name='occupation',
            name='occupation',
            field=models.CharField(unique=True, max_length=150),
        ),
        migrations.AlterField(
            model_name='provider',
            name='primary_institution',
            field=models.CharField(blank=True, null=True, verbose_name='Primary institution', unique=True, max_length=255),
        ),
        migrations.AlterUniqueTogether(
            name='campus',
            unique_together=set([('campus', 'provider')]),
        ),
        migrations.AddField(
            model_name='step',
            name='step_detail',
            field=models.ForeignKey(to='feti.StepDetail', default=None),
        ),
        migrations.AlterUniqueTogether(
            name='stepdetail',
            unique_together=set([('title', 'detail')]),
        ),
    ]
