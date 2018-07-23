# coding=utf-8
"""URI Routing configuration for this apps."""
from django.conf.urls import patterns, url

# Needed by haystack views
from feti.forms.search import DefaultSearchForm
from haystack.query import SearchQuerySet
from haystack.views import search_view_factory, SearchView
from feti.views.campus import UpdateCampusView
from feti.views.feedback import FeedbackInputView, FeedbackSubmittedView
from feti.views.provider import UpdateProviderView
from feti.views.landing_page import EmbedPage, LandingPage
from feti.views.api import (
    ApiAutocomplete,
    ApiOccupation,
    ApiSavedCampus
)
from feti.api_views.campus import (
    ApiCampus,
    CampusSummary
)
from feti.api_views.course import (
    CourseAPIView,
    ApiCourseIds
)
from feti.api_views.occupation_provider import ApiOccupationCampus
from feti.api_views.occupation import(
    OccupationListApiView
)
from feti.api_views.subfield_of_study import (
    SubFieldOfStudyAPIView
)
from feti.api_views.field_of_study import (
    FieldOfStudyAPIView
)
from feti.api_views.qualification_type import (
    QualificationTypeAPIView
)
from feti.api_views.national_qualifications_framework import (
    NationalQualificationsFrameworkAPIView
)
from feti.api_views.national_qualifications_subframework import (
    NationalQualificationsSubFrameworkAPIView
)
from feti.views.share import PDFDownload, EmailShare, ApiRandomString, ApiGetURL
from feti.views.travel_time import TravelTime
from feti.views.jasmine import JasmineView
from django.conf import settings

# custom metrics -- from prometheus_feti app
from .prometheus_feti.counter import PrometheusCounter
# from .prometheus_feti.response_time import cpuinfo
sqs = SearchQuerySet()

api_urls = patterns(
    '',
    url(
        r'^api/saved-campus/$',
        ApiSavedCampus.as_view(),
        name='api-saved-campus'),
    url(
        r'^api/campus$',
        ApiCampus.as_view(),
        name='api-campus'),
    url(
        r'^api/course$',
        CourseAPIView.as_view(),
        name='api-course'),
    url(
        r'^api/occupation$',
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
        r'^api/get-courses/',
        ApiCourseIds.as_view(),
        name='api-get-courses'
    ),
    url(
        r'^api/detail-campus/',
        CampusSummary.as_view(),
        name='api-get-campus-detail'
    ),
    url(
        r'^url/(?P<random>[\w\d]+)',
        ApiGetURL.as_view(),
        name="api-get-url"
    ),
    url(
        r'^api/subfield_of_study$',
        SubFieldOfStudyAPIView.as_view(),
        name="api-get-subfield-of-study"
    ),
    url(
        r'^api/field_of_study$',
        FieldOfStudyAPIView.as_view(),
        name="api-get-field-of-study"
    ),
    url(
        r'^api/qualification_type$',
        QualificationTypeAPIView.as_view(),
        name="api-get-qualification-type"
    ),
    url(
        r'^api/national_qualifications_framework$',
        NationalQualificationsFrameworkAPIView.as_view(),
        name="api-get-nqf"
    ),
    url(
        r'^api/national_qualifications_subframework$',
        NationalQualificationsSubFrameworkAPIView.as_view(),
        name="api-get-nqsf"
    ),
    url(
        r'^api/list_occupation/',
        OccupationListApiView.as_view(),
        name='api-get-occupation-list'),
    url(
        r'api/course-by-occupation$',
        ApiOccupationCampus.as_view(),
        name='api-occupation-course')
)

urlpatterns = patterns(
    '',
    url(
        r'^$',
        LandingPage.as_view(),
        name='landing_page'),
    url(
        r'^embed/',
        EmbedPage.as_view(),
        name='embed_page'),
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
    url(regex='^pdf_report/(?P<resource>.*)',
        view=PDFDownload.as_view()),    
    url(regex='^share_email/',
        view=EmailShare.as_view(),
        name='send_email'),
    url(regex='^primary-institute/(?P<pk>\d+)/update/$',
        view=UpdateProviderView.as_view(),
        name='primary_institute_campus'),
    url(regex='^leave-feedback/$',
        view=FeedbackInputView.as_view(),
        name='input-feedback'),
    url(regex='^feedback-submitted/$',
        view=FeedbackSubmittedView.as_view(),
        name='success_view'),
        #
        # # custom metric exporters
        # url(regex = '^metrics/$',
        #     view = cpuinfo,
        #     name = 'process_uptime_total_custom'),
        # #

) + api_urls

if settings.DEBUG:
    urlpatterns += patterns(
        '',
        url(r'jasmine', JasmineView.as_view())
    )
