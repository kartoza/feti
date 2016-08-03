# coding=utf-8
from feti.models.national_qualifications_framework import \
    NationalQualificationsFramework
from haystack import indexes

__author__ = 'Rizky Maulana Nugraha "lucernae" <lana.pcfre@gmail.com>'
__date__ = '24/04/15'


class NationalQualificationsFrameworkIndex(indexes.SearchIndex,
                                           indexes.Indexable):
    text = indexes.EdgeNgramField(document=True, use_template=True)
    certification = indexes.CharField(model_attr='certification')

    class Meta:
        app_label = 'feti'

    def get_model(self):
        return NationalQualificationsFramework

    def index_queryset(self, using=None):
        """Used to reindex model"""
        return self.get_model().objects.all()
