# coding=utf-8
from feti.models.national_graduate_school_in_education import \
    NationalGraduateSchoolInEducation
from haystack import indexes

__author__ = 'Rizky Maulana Nugraha "lucernae" <lana.pcfre@gmail.com>'
__date__ = '24/04/15'


class NationalGraduateSchoolInEducationIndex(indexes.SearchIndex,
                                         indexes.Indexable):
    text = indexes.EdgeNgramField(document=True, use_template=True)

    class Meta:
        app_label = 'feti'

    def get_model(self):
        return NationalGraduateSchoolInEducation

    def index_queryset(self, using=None):
        """Used to reindex model"""
        return self.get_model().objects.all()