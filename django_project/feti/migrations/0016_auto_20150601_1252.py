# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('feti', '0015_auto_20150601_1251'),
    ]

    operations = [
        migrations.AlterField(
            model_name='course',
            name='education_training_quality_assurance',
            field=models.ForeignKey(blank=True, to='feti.EducationTrainingQualityAssurance', null=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='course',
            name='national_certificate_vocational',
            field=models.ForeignKey(blank=True, to='feti.NationalCertificateVocational', null=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='course',
            name='national_graduate_school_in_education',
            field=models.ForeignKey(blank=True, to='feti.NationalGraduateSchoolInEducation', null=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='course',
            name='national_qualifications_framework',
            field=models.ForeignKey(blank=True, to='feti.NationalQualificationsFramework', null=True),
            preserve_default=True,
        ),
    ]
