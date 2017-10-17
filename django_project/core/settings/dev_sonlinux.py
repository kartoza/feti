# -*- coding: utf-8 -*-
from .dev import *  # noqa

DATABASES = {
    'default': {
        'ENGINE': 'django.contrib.gis.db.backends.postgis',
        'NAME': 'feti',
        'USER': 'alison',
        'PASSWORD': 'M2kr00t',
        'HOST': 'localhost',
        # Set to empty string for default.
        # 'PORT': '5433',
    }
}

# Local static path
STATIC_ROOT = '/home/cyborg/Documents/development@kartoza/feti_static'
# URL prefix for static files.
# Example: "http://example.com/static/", "http://static.example.com/"
STATIC_URL = '/static/'

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        # define output formats
        'verbose': {
            'format': (
                '%(levelname)s %(name)s %(asctime)s %(module)s %(process)d '
                '%(thread)d %(message)s')
        },
        'simple': {
            'format': (
                '%(name)s %(levelname)s %(filename)s L%(lineno)s: '
                '%(message)s')
        },
    },
    'handlers': {
        # console output
        'console': {
            'class': 'logging.StreamHandler',
            'formatter': 'simple',
            'level': 'DEBUG',
        },
        # 'logfile': {
        #     'class': 'logging.FileHandler',
        #     'filename': '/tmp/app-dev.log',
        #     'formatter': 'simple',
        #     'level': 'DEBUG',
        # }
    },
    'loggers': {
        'django.db.backends': {
            'handlers': ['console'],
            'level': 'INFO',  # switch to DEBUG to show actual SQL
        },
        # example app logger
        'localities': {
            'level': 'DEBUG',
            'handlers': ['console'],
            # propagate is True by default, which proppagates logs upstream
            'propagate': False
        }
    },
    # root logger
    # non handled logs will propagate to the root logger
    'root': {
        'handlers': ['console'],
        'level': 'WARNING'
    }
}


HAYSTACK_CONNECTIONS = {
    'default': {
        'ENGINE': 'feti.search_backends.fuzzy_elastic_search_engine'
                  '.FuzzyElasticSearchEngine',
        'URL': 'http://localhost:9200/',
        'INDEX_NAME': 'haystack',
    },
}
