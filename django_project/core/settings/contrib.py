# -*- coding: utf-8 -*-
from .base import *  # noqa
import os

# Extra installed apps
INSTALLED_APPS += (
    'raven.contrib.django.raven_compat',  # enable Raven plugin
    'pipeline',
    'rest_framework',
    'rest_framework_gis',
    'haystack',
    'leaflet',
    'djgeojson',
    'nested_inline',
    'crispy_forms',
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'celery',
)

SITE_ID = 1
PIPELINE = dict()
# These get enabled in prod.py
PIPELINE['PIPELINE_ENABLED'] = False

STATICFILES_STORAGE = 'pipeline.storage.PipelineCachedStorage'

STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    'pipeline.finders.PipelineFinder',
)
MIDDLEWARE_CLASSES += (
    'django.middleware.gzip.GZipMiddleware',
)
TEMPLATE_CONTEXT_PROCESSORS = (
    'django.contrib.auth.context_processors.auth',
    'django.core.context_processors.request',
    'django.contrib.messages.context_processors.messages',
    'django.core.context_processors.media',
)

LEAFLET_CONFIG = {
    'TILES': [
        (
            'OpenStreetMap',
            'http://{s}.tile.openstreetmap.fr/hot/{z}/{x}/{y}.png',
            ('© <a href="http://www.openstreetmap.org" '
             'target="_parent">OpenStreetMap</a> and contributors, under an '
             '<a href="http://www.openstreetmap.org/copyright" '
             'target="_parent">open license</a>')
        )]

}

HAYSTACK_DEFAULT_OPERATOR = 'AND'
HAYSTACK_SIGNAL_PROCESSOR = 'haystack.signals.RealtimeSignalProcessor'

GRAPPELLI_ADMIN_TITLE = 'Feti Administration'
CRISPY_TEMPLATE_PACK = 'bootstrap3'

try:
    BROKER_URL = 'amqp://guest:guest@%s:5672//' % os.environ['RABBITMQ_HOST']
except KeyError:
    pass

CELERY_ACCEPT_CONTENT = ['json']
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'

ACCOUNT_USERNAME_VALIDATORS = 'feti.validators.username_validator.UsernameValidator'
