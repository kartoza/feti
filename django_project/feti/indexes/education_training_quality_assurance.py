# coding=utf-8
from feti.models.education_training_quality_assurance import \
    EducationTrainingQualityAssurance
from haystack import indexes

__author__ = 'Rizky Maulana Nugraha "lucernae" <lana.pcfre@gmail.com>'
__date__ = '24/04/15'


class EducationTrainingQualityAssuranceIndex(indexes.SearchIndex,
                                             indexes.Indexable):
    text = indexes.EdgeNgramField(document=True, use_template=True)
    acronym = indexes.CharField(model_attr='acronym')
    body_name = indexes.CharField(model_attr='body_name')

    class Meta:
        app_label = 'feti'

    def get_model(self):
        return EducationTrainingQualityAssurance

    def index_queryset(self, using=None):
        """Used to reindex model"""
        return self.get_model().objects.all()