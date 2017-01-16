# coding=utf-8
from feti.models.campus import Campus
from haystack import indexes

__author__ = 'Rizky Maulana Nugraha "lucernae" <lana.pcfre@gmail.com>'
__date__ = '24/04/15'


class CampusIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)
    campus = indexes.NgramField(model_attr='campus', indexed=True)
    long_description = indexes.NgramField(
        model_attr='_long_description',
        null=True
    )
    campus_provider = indexes.NgramField(
        model_attr='provider'
    )
    campus_location_isnull = indexes.BooleanField()
    courses_isnull = indexes.BooleanField()
    campus_location = indexes.LocationField(
        model_attr='location',
        null=True
    )
    campus_address = indexes.CharField(
        model_attr='address__address_line',
        null=True
    )
    campus_website = indexes.CharField(
        model_attr='provider__website',
        null=True
    )
    campus_auto = indexes.EdgeNgramField(model_attr='campus')

    provider_primary_institution = indexes.EdgeNgramField()
    courses = indexes.CharField()
    courses_id = indexes.CharField()

    def prepare_campus_location_isnull(self, obj):
        return obj.location is None

    def prepare_courses_isnull(self, obj):
        return obj.courses is None

    def prepare_provider_primary_institution(self, obj):
        return obj.provider.primary_institution

    def prepare_courses(self, obj):
        return [l.course_description for l in obj.courses.all()]

    def prepare_courses_id(self, obj):
        return [l.id for l in obj.courses.all()]

    class Meta:
        app_label = 'feti'

    def get_model(self):
        return Campus

    def index_queryset(self, using=None):
        """Used to reindex model"""
        return self.get_model().objects.all()
