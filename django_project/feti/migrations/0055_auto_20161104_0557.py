# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('feti', '0054_auto_20161103_0524'),
    ]

    operations = [
        migrations.CreateModel(
            name='AbetBand',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='ID', auto_created=True, primary_key=True)),
                ('band', models.CharField(max_length=150)),
            ],
        ),
        migrations.CreateModel(
            name='NationalQualificationFrameworkSubFramework',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='ID', auto_created=True, primary_key=True)),
                ('code', models.CharField(max_length=50)),
                ('title', models.CharField(blank=True, null=True, max_length=150)),
            ],
        ),
        migrations.CreateModel(
            name='Pre2009NationalQualificationsFramework',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='ID', auto_created=True, primary_key=True)),
                ('level', models.CharField(max_length=150)),
            ],
        ),
        migrations.CreateModel(
            name='QualClass',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='ID', auto_created=True, primary_key=True)),
                ('title', models.CharField(max_length=150)),
            ],
        ),
        migrations.CreateModel(
            name='QualificationType',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='ID', auto_created=True, primary_key=True)),
                ('type', models.CharField(max_length=150)),
            ],
        ),
        migrations.CreateModel(
            name='SubFieldOfStudy',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='ID', auto_created=True, primary_key=True)),
                ('learning_subfield', models.CharField(max_length=150)),
            ],
        ),
        migrations.AddField(
            model_name='course',
            name='articulation_options',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='course',
            name='associated_assessment_criteria',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='course',
            name='criteria_for_the_registration_of_assessors',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='course',
            name='exit_level_outcomes',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='course',
            name='international_comparability',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='course',
            name='last_date_for_achievement',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='course',
            name='last_date_for_enrolment',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='course',
            name='learning_assumed_to_be_in_place_and_recognition',
            field=models.TextField(blank=True, verbose_name='Learning Assumed To Be In Place And Recognition Of Prior Learning', null=True),
        ),
        migrations.AddField(
            model_name='course',
            name='minimum_credits',
            field=models.PositiveIntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='course',
            name='moderation_options',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='course',
            name='notes',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='course',
            name='purpose_and_rationale_of_the_qualification',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='course',
            name='qualification_rules',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='course',
            name='recognise_previous_learning',
            field=models.NullBooleanField(default=None),
        ),
        migrations.AddField(
            model_name='course',
            name='registration_end_date',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='course',
            name='registration_start_date',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='course',
            name='registration_status',
            field=models.NullBooleanField(default=None),
        ),
        migrations.AddField(
            model_name='course',
            name='reregistration_history',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='course',
            name='saqa_decision_number',
            field=models.CharField(blank=True, null=True, max_length=150),
        ),
        migrations.AlterField(
            model_name='stepdetail',
            name='course',
            field=models.ManyToManyField(blank=True, to='feti.Course'),
        ),
        migrations.AddField(
            model_name='course',
            name='abet_band',
            field=models.ForeignKey(blank=True, null=True, to='feti.AbetBand'),
        ),
        migrations.AddField(
            model_name='course',
            name='national_qualifications_subframework',
            field=models.ForeignKey(blank=True, null=True, to='feti.NationalQualificationFrameworkSubFramework'),
        ),
        migrations.AddField(
            model_name='course',
            name='pre_2009_national_qualifications_framework',
            field=models.ForeignKey(blank=True, null=True, to='feti.Pre2009NationalQualificationsFramework'),
        ),
        migrations.AddField(
            model_name='course',
            name='qual_class',
            field=models.ForeignKey(blank=True, null=True, to='feti.QualClass'),
        ),
        migrations.AddField(
            model_name='course',
            name='qualification_type',
            field=models.ForeignKey(blank=True, null=True, to='feti.QualificationType'),
        ),
        migrations.AddField(
            model_name='course',
            name='subfield_of_study',
            field=models.ForeignKey(blank=True, null=True, to='feti.SubFieldOfStudy'),
        ),
    ]
