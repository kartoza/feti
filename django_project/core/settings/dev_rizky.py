# -*- coding: utf-8 -*-
from core.settings.utils import DJANGO_ROOT
from .dev import *  # noqa
import os

ADMINS = (
    ('Tim Sutton', 'tim@kartoza.com'),
    ('Ismail Sunni', 'ismail@kartoza.com'),
    ('Christian Christelis', 'christian@kartoza.com'),
    ('Rizky Maulana Nugraha', 'lana.pcfre@gmail.com'))

DATABASES = {
    'default': {
        'ENGINE': 'django.contrib.gis.db.backends.postgis',
        'NAME': 'gis',
        'USER': 'docker',
        'PASSWORD': 'docker',
        'HOST': 'localhost',
        # Set to empty string for default.
        'PORT': '6543',
        'TEST_NAME': 'unittests',
    }
}

# MEDIA_ROOT = '/home/web/media'
STATIC_ROOT = '%s/feti/static' % DJANGO_ROOT

# See fig.yml file for postfix container definition
#
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
# Host for sending e-mail.
EMAIL_HOST = 'smtp'
# Port for sending e-mail.
EMAIL_PORT = 25
# SMTP authentication information for EMAIL_HOST.
# See fig.yml for where these are defined
EMAIL_HOST_USER = 'noreply@kartoza.com'
EMAIL_HOST_PASSWORD = 'docker'
EMAIL_USE_TLS = False
EMAIL_SUBJECT_PREFIX = '[feti]'

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
        'applogfile': {
            'level': 'DEBUG',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': os.path.join(DJANGO_ROOT, 'feti.log'),
            'maxBytes': 1024*1024*15,  # 15MB
            'backupCount': 10,
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
        },
        'feti': {
            'handlers': ['applogfile'],
            'level': 'DEBUG',
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
        'ENGINE': 'haystack.backends.elasticsearch_backend.ElasticsearchSearchEngine',
        'URL': 'http://localhost:9200/',
        'INDEX_NAME': 'haystack',
    },
}
