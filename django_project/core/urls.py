# -*- coding: utf-8 -*-
from django.conf.urls import patterns, include, url
from django.conf import settings

from django.contrib import admin


urlpatterns = patterns(
    '',

    # Enable the admin:
    url(r'^accounts/login/$', 'user_profile.views.login'),
    url(r'^accounts/logout/$', 'user_profile.views.logout'),
    url(r'^feti-admin/', include(admin.site.urls)),

    # include application urls
    url(r'', include('feti.urls')),

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
