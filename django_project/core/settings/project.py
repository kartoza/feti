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
            'js/jquery-1.11.3.min.js',
            'js/bootstrap.js',
            'js/moment.min.js',
            'feti/js/libs/Leaflet/0.7.7/leaflet.js',
            'feti/js/libs/ripples.min.js',
            'feti/js/libs/validate.js',
            'feti/leaflet-extra-markers/leaflet.extra-markers.js',
            'feti/js/libs/underscore-1.8.3.min.js',
            'feti/js/libs/backbone-1.3.3.min.js',
            'feti/js/libs/jquery-ui-1.12.0.min.js',
            'feti/js/libs/leaflet.draw-0.3.2/leaflet.draw.js',
        ),
        'output_filename': 'js/contrib.js',
    },
    'appjs': {
        'source_filenames': (
            'feti/js/libs/leaflet.control.share.js',
            'js/csrf-ajax.js',
            'feti/js/libs/require.min.js',
        ),
        'output_filename': 'js/appjs.js'
    },
    'grappelli_override': {
        'source_filenames': (
            'feti/js/libs/grappelli_override.js',
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
            'feti/js/libs/leaflet.draw-0.3.2/leaflet.draw.css',
        ),
        'output_filename': 'css/contrib.css',
        'extra_context': {
            'media': 'screen, projection',
        },
    },
    'feti-base': {
        'source_filenames': (
            'feti/css/feti-base.css',
        ),
        'output_filename': 'css/feti-base.css',
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
    },
    'custom_page': {
        'source_filenames': (
            'feti/css/feti-custom-page.css',
        ),
        'output_filename': 'css/custom-page.css',
        'extra_context': {
            'media': 'screen, projection',
        },
    }
}

# Cache folder
CACHE_DIR = ABS_PATH('cache')
