# coding=utf-8
"""URI Routing configuration for this apps."""
from django.conf.urls import patterns, url

# Needed by haystack views
from feti.forms.search import DefaultSearchForm
from haystack.query import SearchQuerySet
from haystack.views import search_view_factory, SearchView
from feti.views.campus import UpdateCampusView
from feti.views.provider import UpdateProviderView
from feti.views.landing_page import LandingPage
from feti.views.api import (
    ApiCampus,
    ApiCourse,
    ApiAutocomplete,
    ApiOccupation,
    ApiSavedCampus
)
from feti.api_views.campus import AllCampus
from feti.api_views.course import ApiCourseIds
from feti.views.share import PDFDownload, EmailShare, ApiRandomString, ApiGetURL
from feti.views.travel_time import TravelTime

sqs = SearchQuerySet()

api_urls = patterns(
    '',
    url(
        r'^api/saved-campus/',
        ApiSavedCampus.as_view(),
        name='api-saved-campus'),
    url(
        r'^api/campus',
        ApiCampus.as_view(),
        name='api-campus'),
    url(
        r'^api/course',
        ApiCourse.as_view(),
        name='api-campus'),
    url(
        r'^api/occupation',
        ApiOccupation.as_view(),
        name='api-occupation'),
    url(
        r'^api/autocomplete/(?P<model>.+)',
        ApiAutocomplete.as_view(),
        name='api-campus-autocomplete'),
    url(
        r'^api/travel-time/(?P<origin>[\w\d]+)/(?P<destination>[\w\d]+)',
        TravelTime.as_view(),
        name='api-travel-time'),
    url(
        r'^api/travel-time/(?P<origin>[/(-?\d+\.\d+),(-?\d+\.\d+)/]+)/(?P<destination>[/(-?\d+\.\d+),(-?\d+\.\d+)/]+)',
        TravelTime.as_view(),
        name='api-travel-time-coordinates'),
    url(
        r'^api/travel-time-seconds/(?P<origin>[\w\d]+)/(?P<destination>[\w\d]+)',
        TravelTime.as_view(response_type='data'),
        name='api-travel-time-seconds'),
    url(
        r'^api/generate-random-string/',
        ApiRandomString.as_view(),
        name="api-get-random-string"
    ),
    url(
        r'^api/get-all-campus/',
        AllCampus.as_view(),
        name='api-get-all-campus'
    ),
    url(
        r'^api/get-courses/',
        ApiCourseIds.as_view(),
        name='api-get-courses'
    ),
    url(
        r'^url/(?P<random>[\w\d]+)',
        ApiGetURL.as_view(),
        name="api-get-url"
    )
)

urlpatterns = patterns(
    '',
    url(
        r'^$',
        LandingPage.as_view(),
        name='landing_page'),
    url(
        r'^search/',
        # include('haystack.urls')),
        'feti.views.search.search'),
    url(
        r'^customsearch/',
        search_view_factory(
            view_class=SearchView,
            template='search/custom_search.html',
            searchqueryset=sqs,
            form_class=DefaultSearchForm),
        name='haystack_search'),
    url(regex='^provider/(?P<pk>\d+)/update/$',
        view=UpdateCampusView.as_view(),
        name='update_campus'),
    url(regex='^pdf_report/(?P<provider>[\w-]+)/(?P<query>[\w\=, ]+)',
        view=PDFDownload.as_view(),
        name='get_pdf'),
    url(regex='^share_email/',
        view=EmailShare.as_view(),
        name='send_email'),
    url(regex='^primary-institute/(?P<pk>\d+)/update/$',
        view=UpdateProviderView.as_view(),
        name='primary_institute_campus'),
) + api_urls
