# coding=utf-8
"""URI Routing configuration for this apps."""
from django.conf.urls import patterns, url, include

# Needed by haystack views
from feti.forms.search import DefaultSearchForm
from haystack.query import SearchQuerySet
from haystack.views import search_view_factory, SearchView

sqs = SearchQuerySet()

urlpatterns = patterns(
    '',
    url(
        r'^$',
        'feti.views.landing_page.landing_page'
    ),
    url(
        r'^project-team/add-campus/$',
        'feti.views.add_campus.add_campus'
    ),
    url(
        r'^search/',
        include('haystack.urls')
    ),
    url(
        r'^customsearch/',
        search_view_factory(
            view_class=SearchView,
            template='search/custom_search.html',
            searchqueryset=sqs,
            form_class=DefaultSearchForm),
        name='haystack_search'),
)
