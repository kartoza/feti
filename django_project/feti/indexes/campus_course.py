# coding=utf-8
from feti.models.campus_course_entry import CampusCourseEntry
from haystack import indexes

__author__ = 'Rizky Maulana Nugraha "lucernae" <lana.pcfre@gmail.com>'
__date__ = '24/07/15'


class CampusCourseIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)
    campus_campus = indexes.NgramField(
        model_attr='campus__campus', indexed=True
    )
    campus_location_isnull = indexes.BooleanField()
    campus_location = indexes.LocationField(
        model_attr='campus__location',
        null=True
    )
    courses_isnull = indexes.BooleanField()
    campus_provider = indexes.NgramField(
        model_attr='campus__provider'
    )
    course_long_description_auto = indexes.EdgeNgramField(
        model_attr='course__long_description'
    )

    course_course_description = indexes.EdgeNgramField(
        model_attr='course__course_description'
    )

    course_nlrd = indexes.CharField(
        model_attr='course__national_learners_records_database',
        null=True
    )

    def prepare_campus_location_isnull(self, obj):
        return obj.campus.location is None

    def prepare_courses_isnull(self, obj):
        return obj.campus.courses is None

    class Meta:
        app_label = 'feti'

    def get_model(self):
        return CampusCourseEntry

    def index_queryset(self, using=None):
        """Used to reindex model"""
        return self.get_model().objects.all()
