# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.core.validators
import django.contrib.gis.db.models.fields


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Address',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('address_line_1', models.CharField(max_length=100)),
                ('address_line_2', models.CharField(max_length=100)),
                ('address_line_3', models.CharField(max_length=100)),
                ('town', models.CharField(max_length=100)),
                ('postal_code', models.CharField(max_length=4, validators=[django.core.validators.RegexValidator(regex=b'^\\d{4,4}$', message=b'Postal code consists of 4 digits.')])),
                ('phone', models.CharField(blank=True, max_length=12, null=True, validators=[django.core.validators.RegexValidator(regex=b'^\\+\\d{12,12}$', message=b"Phone number should have the following format: '+27888888888'.")])),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Campus',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True)),
                ('campus', models.CharField(max_length=100, null=True, blank=True)),
                ('location', django.contrib.gis.db.models.fields.PointField(srid=4326)),
                ('address', models.ForeignKey(to='feti.Address')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Course',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True)),
                ('national_learners_records_database', models.CharField(help_text=b'National Learners` Records Database (NLRD)', max_length=15, validators=[django.core.validators.RegexValidator(regex=b'^\\d{15,15}$', message=b"National Learners Records Database: '123456789012345'.")])),
                ('course_description', models.CharField(max_length=100, null=True, blank=True)),
            ],
            options={
                'managed': True,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='CourseProviderLink',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True)),
                ('campus', models.ForeignKey(to='feti.Campus')),
                ('course', models.ForeignKey(to='feti.Course')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='EducationTrainingQualityAssurance',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('acronym', models.CharField(max_length=30)),
                ('body_name', models.CharField(max_length=255)),
                ('url', models.URLField()),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='FieldOfStudy',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True)),
                ('field_of_study_class', models.IntegerField()),
                ('field_of_study_description', models.CharField(max_length=50, null=True, blank=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='NationalCertificateVocational',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True)),
                ('national_certificate_vocational_level', models.IntegerField()),
                ('national_certificate_vocational_description', models.CharField(max_length=50, null=True, blank=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='NationalGraduateSchoolInEducation',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True)),
                ('level', models.CharField(max_length=2)),
                ('description', models.CharField(max_length=100)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='NationalQualificationsFramework',
            fields=[
                ('level', models.IntegerField(serialize=False, primary_key=True)),
                ('description', models.CharField(max_length=50)),
                ('certification', models.CharField(max_length=4)),
                ('link', models.URLField()),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Provider',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True)),
                ('primary_institution', models.CharField(max_length=100)),
                ('website', models.URLField()),
                ('status', models.BooleanField(default=True)),
                ('provider_address', models.ForeignKey(to='feti.Address')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='course',
            name='education_training_quality_assurance',
            field=models.ForeignKey(to='feti.EducationTrainingQualityAssurance'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='course',
            name='field_of_study',
            field=models.ForeignKey(to='feti.FieldOfStudy'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='course',
            name='national_certificate_vocational',
            field=models.ForeignKey(to='feti.NationalCertificateVocational'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='course',
            name='national_graduate_school_in_education',
            field=models.ForeignKey(to='feti.NationalGraduateSchoolInEducation'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='course',
            name='national_qualifications_framework',
            field=models.ForeignKey(to='feti.NationalQualificationsFramework'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='campus',
            name='provider',
            field=models.ForeignKey(to='feti.Provider'),
            preserve_default=True,
        ),
    ]
