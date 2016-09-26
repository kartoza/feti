# coding=utf-8
from feti.models.occupation import Occupation
from haystack import indexes

__author__ = 'Irwan Fathurrahman <irwan@kartoza.com>'
__date__ = '26/09/16'
__license__ = "GPL"
__copyright__ = 'kartoza.com'


class OccupationIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)
    occupation = indexes.NgramField(
        model_attr='occupation',
        null=True
    )

    class Meta:
        app_label = 'feti'

    def get_model(self):
        return Occupation

    def index_queryset(self, using=None):
        """Used to reindex model"""
        return self.get_model().objects.all()
