# coding=utf-8
"""Model class for Education and Training Quality Assurance (ETQA)."""
__author__ = 'Christian Christelis <christian@kartoza.com>'
__date__ = '04/2015'
__license__ = "GPL"
__copyright__ = 'kartoza.com'

from django.contrib.gis.db import models
from feti.models.education_training_quality_assurance import (
    EducationTrainingQualityAssurance)


class Course(models.Model):
    national_learners_records_database = models.CharField(
        max_length=255,
        help_text='National Learners` Records Database (NLRD)')
    course_description = models.CharField(
        max_length=100,
        blank=True,
        null=True)
    education_training_quality_assurance = models.ForeignKey(
        EducationTrainingQualityAssurance)



