# coding=utf-8
from django.conf import settings
from feti.models.campus import Campus
from haystack import indexes

from map_administrative.views import get_boundary

__author__ = 'Rizky Maulana Nugraha "lucernae" <lana.pcfre@gmail.com>'
__date__ = '24/04/15'


class CampusIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)
    campus = indexes.NgramField(model_attr='campus', indexed=True)
    long_description = indexes.NgramField(
        model_attr='_long_description',
        null=True
    )
    campus_id = indexes.IntegerField(
        model_attr='id'
    )
    campus_popup = indexes.CharField(
        model_attr='_campus_popup'
    )
    campus_provider = indexes.NgramField(
        model_attr='provider'
    )
    campus_location_is_null = indexes.BooleanField(
        indexed=True
    )
    courses_is_null = indexes.BooleanField(
        indexed=True
    )
    campus_is_null = indexes.BooleanField(
        indexed=True
    )
    campus_location = indexes.LocationField(
        model_attr='location',
        null=True,
        indexed=True
    )
    campus_icon_url = indexes.CharField(
        indexed=True
    )
    campus_address = indexes.CharField(
        model_attr='address__address_line',
        null=True
    )
    campus_website = indexes.CharField(
        model_attr='provider__website',
        null=True
    )
    campus_phone = indexes.CharField(
        model_attr='address__phone',
        null=True,
    )
    campus_auto = indexes.EdgeNgramField(model_attr='campus')
    campus_public_institution = indexes.BooleanField(
        model_attr='provider__status',
        indexed=True,
    )

    provider_primary_institution = indexes.EdgeNgramField()
    courses = indexes.CharField()
    courses_id = indexes.CharField()

    def prepare_campus_location_is_null(self, obj):
        return obj.location is None

    def prepare_courses_is_null(self, obj):
        if obj.courses is None:
            return True
        else:
            if len(obj.courses.filter(national_learners_records_database__isnull=False)) == 0:
                return True
        return False

    def prepare_campus_is_null(self, obj):
        return not obj.campus

    def prepare_provider_primary_institution(self, obj):
        return obj.provider.primary_institution

    def prepare_courses(self, obj):
        return [('%s ;; [%s] %s' % (l.id, l.national_learners_records_database, l.course_description)).replace('\'', '&#39;')
                for l in obj.courses.all() if l.national_learners_records_database is not None]

    def prepare_courses_id(self, obj):
        return [l.id for l in obj.courses.all()]

    def prepare_campus_icon_url(self, obj):
        return obj.provider.icon.url if obj.provider.icon else ''

    def prepare_campus_public_institution(self, obj):
        return obj.provider.status

    class Meta:
        app_label = 'feti'

    def get_model(self):
        return Campus

    def index_queryset(self, using=None):
        """Used to reindex model"""

        if settings.ADMINISTRATIVE:
            boundary = get_boundary(settings.ADMINISTRATIVE)
            if boundary:
                drawn_polygon = boundary.polygon_geometry
                return self.get_model().objects.filter(
                        location__within=drawn_polygon)

        return self.get_model().objects.all()
