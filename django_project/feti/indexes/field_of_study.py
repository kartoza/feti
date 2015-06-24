# coding=utf-8
from feti.models.field_of_study import FieldOfStudy
from haystack import indexes

__author__ = 'Rizky Maulana Nugraha "lucernae" <lana.pcfre@gmail.com>'
__date__ = '24/04/15'


class FieldOfStudyIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.EdgeNgramField(document=True, use_template=True)

    class Meta:
        app_label = 'feti'

    def get_model(self):
        return FieldOfStudy

    def index_queryset(self, using=None):
        """Used to reindex model"""
        return self.get_model().objects.all()