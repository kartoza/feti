# coding=utf-8
from haystack import indexes
from feti.models.provider import Provider

__author__ = 'Rizky Maulana Nugraha "lucernae" <lana.pcfre@gmail.com>'
__date__ = '24/04/15'


class ProviderIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)
    primary_institution = indexes.CharField(model_attr='primary_institution')
    website = indexes.CharField(model_attr='website')
    status = indexes.BooleanField(model_attr='status')

    class Meta:
        app_label = 'feti'

    def get_model(self):
        return Provider

    def index_queryset(self, using=None):
        """Used to reindex model"""
        return self.get_model().objects.all()