# coding=utf-8
from feti.search_backends.fuzzy_elastic_backend import FuzzyElasticBackend
from haystack.backends.elasticsearch_backend import ElasticsearchSearchEngine

__author__ = 'Rizky Maulana Nugraha "lucernae" <lana.pcfre@gmail.com>'
__date__ = '13/05/15'


class FuzzyElasticSearchEngine(ElasticsearchSearchEngine):
    backend = FuzzyElasticBackend
