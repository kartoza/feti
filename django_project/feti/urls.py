# coding=utf-8
"""URI Routing configuration for this apps."""
from django.conf.urls import patterns, url, include

# Needed by haystack views
from feti.forms.search import DefaultSearchForm
from haystack.query import SearchQuerySet
from haystack.views import search_view_factory, SearchView
from feti.views.campus import UpdateCampusView
from feti.views.landing_page import LandingPage
from feti.views.api import ApiCampuss, ApiCourses

sqs = SearchQuerySet()

api_urls = patterns(
    '',
    url(
        r'^api/campuss/',
        ApiCampuss.as_view(),
        name='api-campuss'),
    url(
        r'^api/courses/(?P<campus_id>\d+)',
        ApiCourses.as_view(),
        name='api-courses'),
)

urlpatterns = patterns(
    '',
    url(
        r'^$',
        LandingPage.as_view(),
        name='landing_page'
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
    url(regex='^campus/(?P<pk>\d+)/update/$',
        view=UpdateCampusView.as_view(),
        name='update_campus'),
)
) + api_urls
