# coding=utf-8
"""URI Routing configuration for this apps."""
from django.conf.urls import patterns, url
from user_profile.views import ProfilePage

urlpatterns = patterns(
    '',
    url(
        r'^login/',
        'user_profile.views.login',
        name='login_page'
    ),
    url(
        r'^login-modal/',
        'user_profile.views.login_modal',
        name='login_modal'
    ),
    url(
        r'^profile/(?P<username>[\w\-]+)',
        ProfilePage.as_view(),
        name='profile_page'
    )
)
