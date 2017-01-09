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
    'map_administrative',
)

PIPELINE = {
    'STYLESHEETS': {
        'contrib': {
            'source_filenames': (
                'css/bootstrap.min.css',
                'feti/css/leaflet.css',
                'css/bootstrap-datetimepicker.min.css',
                'feti/leaflet-extra-markers/leaflet.extra-markers.css',
                'feti/font-awesome/css/font-awesome.css',
                'feti/js/libs/leaflet.draw-0.4.9/leaflet.draw.css',
                'feti/js/libs/easy-button/easy-button.css',
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
                'feti/css/responsive-tab.css',
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
    },
    'JAVASCRIPT': {
        'contrib': {
            'source_filenames': (
                'js/bootstrap.js',
                'js/moment.min.js',
                'feti/js/libs/Leaflet/0.7.7/leaflet.js',
                'feti/js/libs/ripples.min.js',
                'feti/js/libs/validate.js',
                'feti/leaflet-extra-markers/leaflet.extra-markers.js',
                'feti/js/libs/underscore-1.8.3.min.js',
                'feti/js/libs/backbone-1.3.3.min.js',
                'feti/js/libs/leaflet.draw-0.4.9/leaflet.draw.js',
                'feti/js/libs/easy-button/easy-button.js',
            ),
            'output_filename': 'js/contrib.js',
        },
        'appjs': {
            'source_filenames': (
                'feti/js/libs/leaflet.control.share.js',
                'js/csrf-ajax.js',
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
}

# Cache folder
CACHE_DIR = ABS_PATH('cache')

from .celery_setting import *  # noqa