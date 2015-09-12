# coding=utf-8
from feti.models.campus_course_entry import CampusCourseEntry
from haystack import indexes

__author__ = 'Rizky Maulana Nugraha "lucernae" <lana.pcfre@gmail.com>'
__date__ = '24/07/15'


class CampusCourseIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)
    campus_long_description = indexes.NgramField(
        model_attr='campus__long_description'
    )
    course_long_description = indexes.NgramField(
        model_attr='course__long_description'
    )

    class Meta:
        app_label = 'feti'

    def get_model(self):
        return CampusCourseEntry

    def index_queryset(self, using=None):
        """Used to reindex model"""
        return self.get_model().objects.all()
