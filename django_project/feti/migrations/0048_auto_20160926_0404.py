# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('feti', '0047_profile'),
    ]

    operations = [
        migrations.CreateModel(
            name='StepDetail',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True)),
                ('title', models.CharField(max_length=255, blank=True, null=True)),
                ('detail', models.CharField(max_length=1024, blank=True, null=True)),
                ('course', models.ForeignKey(null=True, blank=True, to='feti.Course')),
            ],
            options={
                'verbose_name_plural': 'steps',
                'verbose_name': 'step',
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
            field=models.ForeignKey(default=None, to='feti.Occupation'),
        ),
        migrations.AddField(
            model_name='step',
            name='learning_pathway',
            field=models.ForeignKey(default=None, to='feti.LearningPathway'),
        ),
        migrations.AlterField(
            model_name='occupation',
            name='occupation',
            field=models.CharField(max_length=150, unique=True),
        ),
        migrations.AlterField(
            model_name='provider',
            name='primary_institution',
            field=models.CharField(max_length=255, verbose_name='Primary institution', blank=True, unique=True, null=True),
        ),
        migrations.AlterUniqueTogether(
            name='campus',
            unique_together=set([('campus', 'provider')]),
        ),
        migrations.AddField(
            model_name='step',
            name='step_detail',
            field=models.ForeignKey(default=None, to='feti.StepDetail'),
        ),
        migrations.AlterUniqueTogether(
            name='stepdetail',
            unique_together=set([('title', 'detail')]),
        ),
    ]
