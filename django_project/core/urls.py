# -*- coding: utf-8 -*-
from django.conf.urls import patterns, include, url
from django.conf import settings

from django.contrib import admin


urlpatterns = patterns(
    '',

    # grappelli URLS
    url(r'^grappelli/', include('grappelli.urls')),
    # Enable the admin:
    url(r'^feti-admin/logout/$', 'user_profile.views.logout', name='logout'),
    url(r'^feti-admin/login/$', 'user_profile.views.login', name='login'),
    url(r'^feti-admin/', include(admin.site.urls)),

    # include application urls
    url(r'', include('feti.urls', namespace='feti')),
    url(r'', include('user_profile.urls', namespace='user_profile')),

    url(r'^custom_admin/jsi18n', 'django.views.i18n.javascript_catalog'),

    # allauth
    url(r'^accounts/', include('allauth.urls')),

)

# expose static files and uploded media if DEBUG is active
if settings.DEBUG:
    urlpatterns += patterns(
        '',
        url(r'^media/(?P<path>.*)$', 'django.views.static.serve',
            {
                'document_root': settings.MEDIA_ROOT,
                'show_indexes': True
            }),
        url(r'', include('django.contrib.staticfiles.urls'))
    )
