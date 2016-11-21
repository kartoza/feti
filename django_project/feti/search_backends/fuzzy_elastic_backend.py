# coding=utf-8
from haystack.backends.elasticsearch_backend import ElasticsearchSearchBackend

__author__ = 'Rizky Maulana Nugraha "lucernae" <lana.pcfre@gmail.com>'
__date__ = '13/05/15'


class FuzzyElasticBackend(ElasticsearchSearchBackend):

    def __init__(self, connection_alias, **connection_options):
        super(FuzzyElasticBackend, self).__init__(
            connection_alias, **connection_options)

    def build_schema(self, fields):
        content_field_name, mapping = super(
            FuzzyElasticBackend, self).build_schema(fields)
        return content_field_name, mapping

    def build_search_kwargs(self, query_string, **kwargs):
        """Build search kwargs with fuzziness.
        """
        search_kwargs = super(FuzzyElasticBackend, self).build_search_kwargs(
            query_string, **kwargs)

        try:
            search_kwargs["sort"]
        except KeyError:
            search_kwargs["sort"] = [{
                "_score": {
                    "order": "desc"
                }
            }]

        if 'query_string' in search_kwargs['query']['filtered']['query']:

            try:
                search_kwargs["min_score"]
            except KeyError:
                if len(search_kwargs['query']['filtered']
                       ['query']['query_string']['query'].split('OR')) > 2:
                    search_kwargs["min_score"] = 0
                else:
                    search_kwargs["min_score"] = 2

            search_kwargs['query']['filtered']['query']['query_string'][
                'fuzziness'] = 'AUTO'

        if 'query_string' in search_kwargs['query']['filtered']['query']:
            search_kwargs['query']['filtered']['query']['query_string'][
                'default_operator'] = 'OR'

        return search_kwargs

    def search(self, query_string, **kwargs):
        search = super(FuzzyElasticBackend, self).search(query_string, **kwargs)
        return search
