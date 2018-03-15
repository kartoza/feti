# -*- coding: utf-8 -*-
from .test import *  # noqa
import os
print(os.environ)

DATABASES = {
    'default': {
        'ENGINE': 'django.contrib.gis.db.backends.postgis',
        'NAME': 'gis',
        'USER': 'docker',
        'PASSWORD': 'docker',
        'HOST': 'db',
        'PORT': 5432,
        'TEST_NAME': 'unittests',
    }
}

HAYSTACK_CONNECTIONS = {
    'default': {
        'ENGINE': 'feti.search_backends.fuzzy_elastic_search_engine'
                  '.FuzzyElasticSearchEngine',
        'URL': 'http://elasticsearch:9200/',
        'INDEX_NAME': 'haystack',
    },
}
