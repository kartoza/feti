import json
from django.test import TestCase
from django.core.management import call_command
from rest_framework.test import APIRequestFactory
from feti.tests.model_factories import (
    CampusFactory,
    AddressFactory,
    ProviderFactory,
    CourseFactory,
    EducationTrainingQualityAssuranceFactory
)
from feti.views.api import (
    ApiCampus,
    ApiCourse,
    ApiAutocomplete
)


class TestApiView(TestCase):
    """ Test Campus Api """

    def setUp(self):
        self.factory = APIRequestFactory()
        self.course = CourseFactory.create(
            course_description=u'science'
        )
        self.campus = CampusFactory.create(
            campus=u'campus_test',
            courses=(self.course,)
        )
        call_command('rebuild_index', '--noinput')

    def test_get_campus_by_query(self):
        view = ApiCampus.as_view()
        request = self.factory.get('/api/campus?q=campus')
        response = view(request)
        self.assertEqual(self.campus.campus, response.data[0]['campus'])

    def test_get_course_by_query(self):
        view = ApiCourse.as_view()
        request = self.factory.get('/api/course?q=scien')
        response = view(request)

        self.assertTrue(len(response.data) > 0)
        self.assertEqual(self.campus.campus, response.data[0]['campus'])


class TestApiAutocomplete(TestCase):
    """ Test Auto Complete API """

    def setUp(self):
        self.factory = APIRequestFactory()
        self.course = CourseFactory.create(
            course_description=u'engineering'
        )
        self.campus = CampusFactory.create(
            campus=u'campus_tests',
            courses=(self.course,)
        )
        call_command('rebuild_index', '--noinput')

    def test_get_autcomplete_campus(self):
        view = ApiAutocomplete.as_view()
        model = 'provider'
        request = self.factory.get('/api/autocomplete/%s?q=cam' % model)
        response = view(request, model)

        response_data = json.loads(response.content.decode('utf-8'))

        self.assertTrue(len(response_data) > 0)
        self.assertEqual(self.campus.campus, response_data[0])
