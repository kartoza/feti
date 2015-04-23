# coding=utf-8
"""URI Routing configuration for this apps."""
from django.conf.urls import patterns, url

urlpatterns = patterns(
    '',
    url(
        r'^$',
        'feti.views.landing_page.landing_page'
    ),
    url(
        r'^/project-team/add-campus/$',
        'feti.views.add_campus.add_campus'
    )
)
