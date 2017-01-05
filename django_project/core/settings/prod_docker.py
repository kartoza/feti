# noinspection PyUnresolvedReferences
from .prod import *  # noqa
import os
print(os.environ)

ALLOWED_HOSTS = ['*']

ADMINS = (
    ('Dimas Ciputra', 'dimas@kartoza.com'),
    ('Irwan Fathurrahman', 'irwan@kartoza.com'),
    ('Christian Christelis', 'christian@kartoza.com'))

DATABASES = {
    'default': {
        'ENGINE': 'django.contrib.gis.db.backends.postgis',
        'NAME': os.environ['DATABASE_NAME'],
        'USER': os.environ['DATABASE_USERNAME'],
        'PASSWORD': os.environ['DATABASE_PASSWORD'],
        'HOST': os.environ['DATABASE_HOST'],
        'PORT': 5432,
        'TEST_NAME': 'unittests',
    }
}

MEDIA_ROOT = '/home/web/media'
STATIC_ROOT = '/home/web/static'

# See docker-compose.yml file for postfix container definition
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

# ELASTIC SEARCH
HAYSTACK_CONNECTIONS = {
    'default': {
        'ENGINE': 'feti.search_backends.fuzzy_elastic_search_engine'
                  '.FuzzyElasticSearchEngine',
        'URL': 'http://%s:9200/' % os.environ['HAYSTACK_HOST'],
        'INDEX_NAME': 'haystack',
    },
}

DEBUG = False
