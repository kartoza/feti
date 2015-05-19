# -*- coding: utf-8 -*-
from .contrib import *  # noqa

DATABASES = {
    'default': {
        # Add 'postgresql_psycopg2', 'mysql', 'sqlite3' or 'oracle'.
        # 'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'ENGINE': 'django.contrib.gis.db.backends.postgis',
        # Or path to database file if using sqlite3.
        'NAME': '',
        # The following settings are not used with sqlite3:
        'USER': '',
        'PASSWORD': '',
        # Empty for localhost through domain sockets or '127.0.0.1' for
        # localhost through TCP.
        'HOST': '',
        # Set to empty string for default.
        'PORT': '',
    }
}

# Project apps
INSTALLED_APPS += (
    'feti',
    'user_profile',
)


PIPELINE_JS = {
    'contrib': {
        'source_filenames': (
            'js/jquery-1.11.1.min.js',
            'js/bootstrap.js',
            'js/moment.min.js',
            'feti/js/leaflet.js',
            'feti/js/leaflet.markercluster.js',
            'feti/js/material.min.js',
            'feti/js/ripples.min.js',
            'feti/js/validate.js',
            'js/bootstrap-datetimepicker.min.js',
            'feti/js/jquery.flot.min.js',
            'feti/js/jquery.flot.time.min.js',
        ),
        'output_filename': 'js/contrib.js',
    },
    'appjs': {
        'source_filenames': (
            'feti/js/feti.js',
            'js/csrf-ajax.js',
        ),
        'output_filename': 'js/appjs.js'
    }
}

PIPELINE_CSS = {
    'contrib': {
        'source_filenames': (
            'css/bootstrap.min.css',
            'feti/css/leaflet.css',
            'feti/css/MarkerCluster.Default.css',
            'feti/css/MarkerCluster.css',
            'feti/css/material-wfont.min.css',
            'feti/css/ripples.min.css',
            'feti/css/feti-theme.css',
            'css/bootstrap-datetimepicker.min.css',
        ),
        'output_filename': 'css/contrib.css',
        'extra_context': {
            'media': 'screen, projection',
        },
    }
}
