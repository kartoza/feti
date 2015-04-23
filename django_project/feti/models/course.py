# coding=utf-8
"""Model class for Education and Training Quality Assurance (ETQA)."""
__author__ = 'Christian Christelis <christian@kartoza.com>'
__date__ = '04/2015'
__license__ = "GPL"
__copyright__ = 'kartoza.com'

from django.contrib.gis.db import models
from django.core.validators import RegexValidator
from feti.models.education_training_quality_assurance import (
    EducationTrainingQualityAssurance)
from feti.models.national_qualifications_framework import (
    NationalQualificationsFramework)
from feti.models.national_graduate_school_in_education import (
    NationalGraduateSchoolInEducation)
from feti.models.national_certificate_vocational import (
    NationalCertificateVocational)
from feti.models.field_of_study import FieldOfStudy


class Course(models.Model):

    id = models.AutoField(primary_key=True)
    nlrd_regex = RegexValidator(
        regex=r'^\d{15,15}$',
        message="National Learners Records Database: "
                "'123456789012345'.")
    national_learners_records_database = models.CharField(
        max_length=15,
        validators=[nlrd_regex],
        help_text='National Learners` Records Database (NLRD)')
    course_description = models.CharField(
        max_length=100,
        blank=True,
        null=True)
    education_training_quality_assurance = models.ForeignKey(
        EducationTrainingQualityAssurance)
    national_qualifications_framework = models.ForeignKey(
        NationalQualificationsFramework)
    national_graduate_school_in_education = models.ForeignKey(
        NationalGraduateSchoolInEducation)
    national_certificate_vocational = models.ForeignKey(
        NationalCertificateVocational)
    field_of_study = models.ForeignKey(FieldOfStudy)

    def __unicode__(self):
        return '%s' % self.national_learners_records_database

    class Meta:
        app_label = 'feti'




