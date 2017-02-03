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
    campus_and_provider = indexes.NgramField(
        model_attr='campus__long_description',
        indexed=True
    )
    campus_location_isnull = indexes.BooleanField()
    campus_id = indexes.IntegerField(
        model_attr='campus__id',
        null=True
    )
    course_id = indexes.IntegerField(
        model_attr='course__id',
        null=True
    )
    campus_location = indexes.LocationField(
        model_attr='campus__location',
        null=True
    )
    courses_isnull = indexes.BooleanField()
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
    campus_popup = indexes.CharField(
        model_attr='campus___campus_popup'
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
