# coding=utf-8
from feti.models.campus_course_entry import CampusCourseEntry
from feti.models.campus import Campus
from haystack import indexes

from django.conf import settings
from map_administrative.views import get_boundary

__author__ = 'Rizky Maulana Nugraha "lucernae" <lana.pcfre@gmail.com>'
__date__ = '24/07/15'


class CampusCourseIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)
    campus_campus = indexes.NgramField(
        model_attr='campus__campus', indexed=True
    )
    campus_and_provider = indexes.NgramField(
        model_attr='campus__long_description',
        indexed=True
    )
    campus_location_isnull = indexes.BooleanField(
        model_attr='campus__location',
        indexed=True
    )
    campus_id = indexes.IntegerField(
        model_attr='campus__id',
        null=True
    )
    course_id = indexes.IntegerField(
        model_attr='course__id',
        null=True
    )

    field_of_study_id = indexes.IntegerField(null=True)
    subfield_of_study_id = indexes.IntegerField(null=True)
    qualification_type_id = indexes.IntegerField(null=True)
    minimum_credits = indexes.IntegerField(
        model_attr='course__minimum_credits',
        null=True
    )
    national_qualifications_framework_id = indexes.IntegerField(null=True)
    national_qualifications_subframework_id = indexes.IntegerField(null=True)

    campus_location = indexes.LocationField(
        model_attr='campus__location',
        null=True
    )
    courses_isnull = indexes.BooleanField(
        indexed=True
    )
    campus_provider = indexes.NgramField(
        model_attr='campus__provider',
        indexed=True
    )
    campus_icon = indexes.CharField(
        model_attr='campus__provider__icon'
    )
    course_course_description = indexes.EdgeNgramField(
        model_attr='course__course_description'
    )
    course_nlrd = indexes.CharField(
        model_attr='course__national_learners_records_database',
        null=True
    )

    campus_address = indexes.CharField(
        model_attr='campus__address__address_line',
        null=True
    )

    campus_website = indexes.CharField(
        model_attr='campus__provider__website',
        null=True
    )
    campus_popup = indexes.CharField(
        model_attr='campus___campus_popup',
        null=True
    )
    campus_public_institution = indexes.BooleanField(
        model_attr='campus__provider__status',
        null=True
    )

    def prepare_field_of_study_id(self, obj):
        try:
            if isinstance(obj.course.field_of_study.id, int):
                return obj.course.field_of_study.id
            else:
                return None
        except AttributeError:
            return None

    def prepare_subfield_of_study_id(self, obj):
        try:
            if isinstance(obj.course.subfield_of_study.id, int):
                return obj.course.subfield_of_study.id
            else:
                return None
        except AttributeError:
            return None

    def prepare_qualification_type_id(self, obj):
        try:
            if isinstance(obj.course.qualification_type.id, int):
                return obj.course.qualification_type.id
            else:
                return None
        except AttributeError:
            return None

    def prepare_national_qualifications_framework_id(self, obj):
        try:
            if isinstance(obj.course.national_qualifications_framework.level, int):
                return obj.course.national_qualifications_framework.level
            else:
                return None
        except AttributeError:
            return None

    def prepare_national_qualifications_subframework_id(self, obj):
        try:
            if isinstance(obj.course.national_qualifications_subframework.id, int):
                return obj.course.national_qualifications_subframework.id
            else:
                return None
        except AttributeError:
            return None

    def prepare_campus_location_isnull(self, obj):
        return obj.campus.location is None

    def prepare_courses_isnull(self, obj):
        if obj.campus.courses is None:
            return True
        else:
            if len(obj.campus.courses.filter(national_learners_records_database__isnull=False)) == 0:
                return True
        return False

    class Meta:
        app_label = 'feti'

    def get_model(self):
        return CampusCourseEntry

    def index_queryset(self, using=None):
        """Used to reindex model"""

        if settings.ADMINISTRATIVE:
            boundary = get_boundary(settings.ADMINISTRATIVE)
            if boundary:
                polygon = boundary.polygon_geometry
                campus = Campus.objects.filter(location__within=polygon)
                return self.get_model().objects.filter(campus__in=campus)

        return self.get_model().objects.all()
