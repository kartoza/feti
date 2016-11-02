# coding=utf-8
"""URI Routing configuration for this apps."""
from django.conf.urls import patterns, url
from user_profile.views.admin import UserAdminPage
from user_profile.views.profile import (
    UserProfileView,
    UpdateUserProfileView,
    UpdateUserCampusView,
    DeleteUserCampusView,
    UpdateUserCampusCourseView
)

urlpatterns = patterns(
    '',
    url(
        r'^login/',
        'user_profile.views.login.login',
        name='login_page'
    ),
    url(
        r'^login-modal/',
        'user_profile.views.login.login_modal',
        name='login_modal'
    ),
    url(
        r'^admin/',
        UserAdminPage.as_view(),
        name='user-admin-page'
    ),
    url(
        r'^profile/(?P<username>[\w\d]+)$',
        UserProfileView.as_view(),
        name='user-profile-view'),
    url(
        r'^profile/update/(?P<pk>\d+)$',
        UpdateUserProfileView.as_view(),
        name='update-user-profile-view'),
    url(
        r'^profile/add-campus/',
        UpdateUserCampusCourseView.as_view(),
        name='update-user-campus-view'),
    url(
        r'^profile/delete-campus/',
        DeleteUserCampusView.as_view(),
        name='delete-user-campus-view'),
)
