import json
from unittest.mock import patch
from django.test import TestCase
from feti.api_views.common_search import CommonSearch
from django.core.management import call_command
from rest_framework.test import APIRequestFactory
from feti.tests.model_factories import (
    CampusFactory,
    AddressFactory,
    ProviderFactory,
    CourseFactory,
)


class TestCommonSearch(TestCase):
    """ Test Search Functionality """

    def setUp(self):
        self.factory = APIRequestFactory()
        self.course = CourseFactory.create(
            course_description=u'science'
        )
        with patch('feti.celery.update_search_index.delay') as mock:
            self.campus = CampusFactory.create(
                    campus=u'campus_tests',
                    long_description=u'campus_tests',
                    courses=(self.course,)
            )
            self.mock = mock
        call_command('rebuild_index', '--noinput')
        self.common_search = CommonSearch()

    def test_process_request(self):
        query_from_request = 'test'
        request_dict = {
            'query': query_from_request,
            'fos': 1,
            'sos': 1,
            'qt': 1,
            'mc': 1,
            'nqf': 1,
            'nqsf': 1,
            'pi': 1
        }

        query, options = self.common_search.process_request(request_dict)
        self.assertEquals(query, query_from_request)
        self.assertEquals(len(options), 9)

    def test_filter_indexed_campus(self):
        query = 'campus_tests'
        campus = self.common_search.filter_indexed_campus(query)
        self.assertEquals(len(campus), 1)

    def test_filter_by_course(self):
        query = 'science'
        campus = self.common_search.filter_by_course(query)
        self.assertEquals(len(campus), 1)
