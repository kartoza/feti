# coding=utf-8
from feti.models.campus import Campus
from haystack import indexes

__author__ = 'Rizky Maulana Nugraha "lucernae" <lana.pcfre@gmail.com>'
__date__ = '24/04/15'


class CampusIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)
    campus = indexes.CharField(model_attr='campus')

    class Meta:
        app_label = 'feti'

    def get_model(self):
        return Campus

    def index_queryset(self, using=None):
        """Used to reindex model"""
        return self.get_model().objects.all()