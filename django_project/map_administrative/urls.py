# coding=utf-8
"""URI Routing configuration for this apps."""
from django.conf.urls import patterns, url
from .views import GetAdministrative

api_urls = patterns(
    '',
    url(
        r'^api/administrative',
        GetAdministrative.as_view(),
        name='api-GetAdministrative'),
)

urlpatterns = patterns(
    '',
) + api_urls
