# coding=utf-8
from haystack.backends.elasticsearch_backend import ElasticsearchSearchBackend

__author__ = 'Rizky Maulana Nugraha "lucernae" <lana.pcfre@gmail.com>'
__date__ = '13/05/15'


class FuzzyElasticBackend(ElasticsearchSearchBackend):

    def __init__(self, connection_alias, **connection_options):
        super(FuzzyElasticBackend, self).__init__(
            connection_alias, **connection_options)

    def build_search_kwargs(self, query_string, **kwargs):
        """Build search kwargs with fuzziness.
        """
        search_kwargs = super(FuzzyElasticBackend, self).build_search_kwargs(
            query_string, **kwargs)
        # RM : add fuzzines args
        # leave this be for now
        # del search_kwargs['query']['filtered']['query']['query_string']
        # search_kwargs['query']['filtered']['query']\
        #     ['fuzzy_like_this'] = {
        #     'like_text': query_string,
        # }
        if 'query_string' in search_kwargs['query']['filtered']['query']:
            search_kwargs['query']['filtered']['query']['query_string']\
                ['fuzziness'] = 2
        return search_kwargs
