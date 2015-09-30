# coding=utf-8
"""Model class for Education and Training Quality Assurance (ETQA)."""

__author__ = 'Christian Christelis <christian@kartoza.com>'
__date__ = '04/2015'
__license__ = "GPL"
__copyright__ = 'kartoza.com'

from django.template import Context, loader
from django.contrib.gis.db import models
from django.core.validators import RegexValidator
from django.db.models.signals import post_save
from django.core import management

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
    # nlrd_regex = RegexValidator(
    #     regex=r'^\d{15,15}$',
    #     message="National Learners Records Database: "
    #             "'123456789012345'.")
    national_learners_records_database = models.CharField(
        max_length=50,
        # max_length=15,
        # validators=[nlrd_regex],
        help_text='National Learners` Records Database (NLRD)',
        blank=True,
        null=True)
    course_description = models.CharField(
        max_length=255,
        blank=True,
        null=True)
    education_training_quality_assurance = models.ForeignKey(
        EducationTrainingQualityAssurance, blank=True, null=True)
    national_qualifications_framework = models.ForeignKey(
        NationalQualificationsFramework, blank=True, null=True)
    national_graduate_school_in_education = models.ForeignKey(
        NationalGraduateSchoolInEducation, blank=True, null=True)
    national_certificate_vocational = models.ForeignKey(
        NationalCertificateVocational, blank=True, null=True)
    field_of_study = models.ForeignKey(FieldOfStudy, blank=True, null=True)

    # Decreasing the number of links needed to other models for descriptions.
    _long_description = models.CharField(
        max_length=510,
        blank=True,
        null=True
    )
    # Decreasing the number of links needed to get popup material
    _course_popup = models.CharField(
        max_length=510,
        blank=True,
        null=True
    )

    objects = models.GeoManager()

    def __unicode__(self):
        course_string = u''
        if self.national_learners_records_database:
            course_string = u'[%s]' % self.national_learners_records_database
        if self.long_description:
            course_string += u' %s' % self.long_description
        return course_string

    @property
    def description(self):
        if self.course_description:
            return self.course_description
        else:
            return 'Description to follow.'

    def save(self, *args, **kwargs):
        # Set up long description
        if self.education_training_quality_assurance.acronym.strip():
            seta = u'%s (%s)' % (
                self.education_training_quality_assurance.body_name.strip() or
                u'',
                self.education_training_quality_assurance.acronym.strip() or
                u''
            )
        else:
            seta = self.education_training_quality_assurance.body_name.strip()

        self._long_description = u'%s : %s' % (
            self.description.strip() or u'',
            seta,

        )

        # set up popup material
        template = loader.get_template('feti/course_popup.html')
        description = self.course_description
        variable = {
            'description': description,
            'seta': seta
        }
        self._course_popup = template.render(Context(variable))

        super(Course, self).save(*args, **kwargs)

    @property
    def long_description(self):
        return self._long_description

    @property
    def course_popup(self):
        return self._course_popup

    class Meta:
        app_label = 'feti'
        managed = True


def regenerate_landing_page(sender, instance, **kwargs):
    management.call_command('full_front_page')


post_save.connect(regenerate_landing_page, sender=Course, dispatch_uid="course_landing_page")

