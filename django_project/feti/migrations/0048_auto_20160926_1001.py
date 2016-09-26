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
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('title', models.CharField(null=True, blank=True, max_length=255)),
                ('detail', models.CharField(null=True, blank=True, max_length=1024)),
                ('course', models.ForeignKey(blank=True, to='feti.Course', null=True)),
            ],
            options={
                'verbose_name_plural': 'steps',
                'managed': True,
                'verbose_name': 'step',
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
            field=models.CharField(unique=True, max_length=150),
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
