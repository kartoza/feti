# coding=utf-8
from feti.models.address import Address
from haystack import indexes

__author__ = 'Rizky Maulana Nugraha "lucernae" <lana.pcfre@gmail.com>'
__date__ = '24/04/15'


class AddressIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)
    town = indexes.CharField(model_attr='town')

    class Meta:
        app_label = 'feti'

    def get_model(self):
        return Address

    def index_queryset(self, using=None):
        """Used to reindex model"""
        return self.get_model().objects.all()