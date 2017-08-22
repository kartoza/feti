# -*- coding: utf-8 -*-
from .contrib import *  # noqa

# Exclude elastic result which have a _score less than the minimum specified in min_score
ELASTIC_MIN_SCORE = 3.5

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
                'feti/css/Leaflet-1.0.3/leaflet.css',
                'css/bootstrap-datetimepicker.min.css',
                'js/libs/leaflet-extra-markers/leaflet.extra-markers.css',
                'feti/font-awesome/css/font-awesome.css',
                'js/libs/leaflet.draw-0.4.9/leaflet.draw.css',
                'js/libs/easy-button/easy-button.css',
                'feti/css/bootstrap-slider-9.7.2/bootstrap-slider.min.css',
                'feti/css/chosen.min.css',
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
        'grappelli_override': {
            'source_filenames': (
                'js/libs/grappelli_override.js',
            ),
            'output_filename': 'js/grappelli_override.min.js'
        }
    }
}

# Cache folder
CACHE_DIR = ABS_PATH('cache')

from .celery_setting import *  # noqa

REQUIRE_JS_PATH = '/static/js/libs/require.min.js'

GRUNT_MODULES = {
    'landing_page': {
        'main': '/static/js/main',
        'optimized': 'js/optimized.js',
    }
}

# Set administrative
ADMINISTRATIVE = 'Western Cape'
