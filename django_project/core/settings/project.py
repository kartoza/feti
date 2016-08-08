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
    # 'user_profile',
)


PIPELINE_JS = {
    'contrib': {
        'source_filenames': (
            'js/jquery-1.11.1.min.js',
            'js/bootstrap.js',
            'js/moment.min.js',
            'feti/js/Leaflet/1.0.0-rc1/leaflet.js',
            'feti/js/jspdf.js',
            'feti/js/ripples.min.js',
            'feti/js/validate.js',
            'js/bootstrap-datetimepicker.min.js',
            'feti/js/jquery.flot.min.js',
            'feti/js/jquery.flot.time.min.js',
            'feti/leaflet-extra-markers/leaflet.extra-markers.js',
            'feti/js/ZeroClipboard.js',
            'feti/js/underscore-min.js',
            'feti/js/backbone-min.js',
        ),
        'output_filename': 'js/contrib.js',
    },
    'appjs': {
        'source_filenames': (
            'feti/js/leaflet.control.share.js',
            'js/csrf-ajax.js',
        ),
        'output_filename': 'js/appjs.js'
    },
    'grappelli_override': {
        'source_filenames': (
            'feti/js/grappelli_override.js',
        ),
        'output_filename': 'js/grappelli_override.min.js'
    }
}

PIPELINE_CSS = {
    'contrib': {
        'source_filenames': (
            'css/bootstrap.min.css',
            'feti/css/leaflet.css',
            'css/bootstrap-datetimepicker.min.css',
            'feti/leaflet-extra-markers/leaflet.extra-markers.css',
            'feti/font-awesome/css/font-awesome.css',
        ),
        'output_filename': 'css/contrib.css',
        'extra_context': {
            'media': 'screen, projection',
        },
    },
    'landing_page': {
        'source_filenames': (
            'feti/css/landing-page.css',
        ),
        'output_filename': 'css/landing-page.css',
        'extra_context': {
            'media': 'screen, projection',
        },
    }
}
