# coding=utf-8
"""Model class for Education and Training Quality Assurance (ETQA)."""

from django.template import Context, loader
from django.contrib.gis.db import models
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
from feti.models.subfield_of_study import SubFieldOfStudy
from feti.models.qualification_type import QualificationType
from feti.models.qual_class import QualClass
from feti.models.national_qualification_framework_subframework import \
    NationalQualificationFrameworkSubFramework
from feti.models.abet_band import AbetBand
from feti.models.pre_2009_national_qualifications_framework import \
    Pre2009NationalQualificationsFramework

__author__ = 'Christian Christelis <christian@kartoza.com>'
__date__ = '04/2015'
__license__ = "GPL"
__copyright__ = 'kartoza.com'


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

    national_qualifications_subframework = models.ForeignKey(
            NationalQualificationFrameworkSubFramework,
            blank=True,
            null=True
    )

    pre_2009_national_qualifications_framework = models.ForeignKey(
            Pre2009NationalQualificationsFramework,
            blank=True,
            null=True
    )

    national_graduate_school_in_education = models.ForeignKey(
        NationalGraduateSchoolInEducation, blank=True, null=True)
    national_certificate_vocational = models.ForeignKey(
        NationalCertificateVocational, blank=True, null=True)
    field_of_study = models.ForeignKey(FieldOfStudy, blank=True, null=True)

    subfield_of_study = models.ForeignKey(
            SubFieldOfStudy,
            blank=True,
            null=True
    )

    abet_band = models.ForeignKey(
        AbetBand,
        blank=True,
        null=True
    )

    minimum_credits = models.PositiveIntegerField(
        blank=True,
        null=True
    )

    qualification_type = models.ForeignKey(
        QualificationType,
        blank=True,
        null=True
    )

    qual_class = models.ForeignKey(
        QualClass,
        blank=True,
        null=True
    )

    registration_status = models.CharField(
        max_length=100,
        blank=True,
        null=True
    )

    saqa_decision_number = models.CharField(
        max_length=150,
        blank=True,
        null=True
    )

    registration_start_date = models.DateField(
        blank=True,
        null=True
    )

    registration_end_date = models.DateField(
        blank=True,
        null=True
    )

    last_date_for_enrolment = models.DateField(
        blank=True,
        null=True
    )

    last_date_for_achievement = models.DateField(
        blank=True,
        null=True
    )

    purpose_and_rationale_of_the_qualification = models.TextField(
        blank=True,
        null=True
    )

    learning_assumed_to_be_in_place_and_recognition = models.TextField(
        verbose_name="Learning Assumed To Be In Place And Recognition Of Prior Learning",
        blank=True,
        null=True
    )

    recognise_previous_learning = models.NullBooleanField(
        blank=True,
        null=True,
        default=None
    )

    qualification_rules = models.TextField(
        blank=True,
        null=True
    )

    exit_level_outcomes = models.TextField(
        blank=True,
        null=True
    )

    associated_assessment_criteria = models.TextField(
        blank=True,
        null=True
    )

    international_comparability = models.TextField(
        blank=True,
        null=True
    )

    articulation_options = models.TextField(
        blank=True,
        null=True
    )

    moderation_options = models.TextField(
        blank=True,
        null=True
    )

    criteria_for_the_registration_of_assessors = models.TextField(
        blank=True,
        null=True
    )

    reregistration_history = models.TextField(
        blank=True,
        null=True
    )

    notes = models.TextField(
        blank=True,
        null=True
    )

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

    def __str__(self):
        return self.__unicode__()

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
        seta = ""
        if self.education_training_quality_assurance:
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


def generate_course_index(sender, instance, **kwargs):
    management.call_command('generate_course_index')
