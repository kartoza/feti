# -*- coding: utf-8 -*-
from .project import *  # noqa

# Hosts/domain names that are valid for this site; required if DEBUG is False
# See https://docs.djangoproject.com/en/1.5/ref/settings/#allowed-hosts
ALLOWED_HOSTS = ['*']

DATABASES = {
    'default': {
        'ENGINE': 'django.contrib.gis.db.backends.postgis',
        'NAME': 'feti_dev',
        'USER': '',
        'PASSWORD': '',
        'HOST': 'localhost',
        # Set to empty string for default.
        'PORT': '',
    }
}

# define template function (example for underscore)
# PIPELINE_TEMPLATE_FUNC = '_.template'

PIPELINE['YUI_BINARY'] = '/usr/bin/yui-compressor'
PIPELINE['JS_COMPRESSOR'] = 'pipeline.compressors.yui.YUICompressor'
PIPELINE['CSS_COMPRESSOR'] = 'pipeline.compressors.yui.YUICompressor'
PIPELINE_YUI_JS_ARGUMENTS = '--nomunge'
PIPELINE_DISABLE_WRAPPER = True

# Comment if you are not running behind proxy
USE_X_FORWARDED_HOST = True

# Set debug to false for production
DEBUG = TEMPLATE_DEBUG = False
#
# if 'raven.contrib.django.raven_compat' in INSTALLED_APPS:
#     print '*********** Setting up sentry logging ************'
#     SENTRY_DSN = (
#         'http://04953c939b7142debcd1ef93f5131a48:'
#         '6e132f90f35e41338677185e5f49672b@sentry.linfiniti.com/16')
#
#     # MIDDLEWARE_CLASSES = (
#     #     'raven.contrib.django.middleware.SentryResponseErrorIdMiddleware',
#     #     'raven.contrib.django.middleware.SentryLogMiddleware',
#     # ) + MIDDLEWARE_CLASSES
#
#     #
#     # Sentry settings - logs exceptions to a database
#     LOGGING = {
#         # internal dictConfig version - DON'T CHANGE
#         'version': 1,
#         'disable_existing_loggers': True,
#         # default root logger - handle with sentry
#         'root': {
#             'level': 'ERROR',
#             'handlers': ['sentry'],
#         },
#         'handlers': {
#             # send email to mail_admins, if DEBUG=False
#             'mail_admins': {
#                 'level': 'ERROR',
#                 'class': 'django.utils.log.AdminEmailHandler'
#             },
#             # sentry logger
#             'sentry': {
#                 'level': 'WARNING',
#                 'class': (
#                     'raven.contrib.django.raven_compat.'
#                     'handlers.SentryHandler'),
#             }
#         },
#         'loggers': {
#             'django.db.backends': {
#                 'level': 'ERROR',
#                 'handlers': ['sentry'],
#                 'propagate': False
#             },
#             'raven': {
#                 'level': 'ERROR',
#                 'handlers': ['mail_admins'],
#                 'propagate': False
#             },
#             'sentry.errors': {
#                 'level': 'ERROR',
#                 'handlers': ['mail_admins'],
#                 'propagate': False
#             },
#             'django.request': {
#                 'handlers': ['mail_admins'],
#                 'level': 'ERROR',
#                 'propagate': True
#             }
#         }
#     }
