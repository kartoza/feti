import json
from django.test import TestCase
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


class TestCampusApiView(TestCase):
    """ Test Campus Api """

    def setUp(self):
        self.factory = APIRequestFactory()

    def test_get_campus_by_query(self):
        campus = CampusFactory.create(
            campus=u'campus_test'
        )
        view = ApiCampus.as_view()
        request = self.factory.get('/api/campus?q=campus')
        response = view(request)

        self.assertEqual(campus.campus, response.data[0]['campus'])


class TestCourseApiView(TestCase):
    """ Test Course API """

    def setUp(self):
        self.factory = APIRequestFactory()

    def test_get_course_by_query(self):
        course = CourseFactory.create(
            course_description=u'science'
        )
        campus = CampusFactory.create(
            courses=(course,)
        )
        view = ApiCourse.as_view()
        request = self.factory.get('/api/course?q=science')
        response = view(request)

        self.assertTrue(len(response.data) > 0)
        self.assertEqual(campus.campus, response.data[0]['campus'])


class TestApiAutocomplete(TestCase):
    """ Test Auto Complete API """

    def setUp(self):
        self.factory = APIRequestFactory()

    def test_get_autcomplete_campus(self):
        campus = CampusFactory.create(
            campus=u'campus_test'
        )
        view = ApiAutocomplete.as_view()
        model = 'provider'
        request = self.factory.get('/api/autocomplete/%s?q=cam' % model)
        response = view(request, model)

        response_data = json.loads(response.content.decode('utf-8'))

        self.assertTrue(len(response_data) > 0)
        self.assertEqual(campus.campus, response_data[0])

    def test_get_autcomplete_course(self):
        course = CourseFactory.create(
            course_description=u'science'
        )
        view = ApiAutocomplete.as_view()
        model = 'course'
        request = self.factory.get('/api/autocomplete/%s?q=scie' % model)
        response = view(request, model)

        response_data = json.loads(response.content.decode('utf-8'))

        self.assertTrue(len(response_data) > 0)
        self.assertEqual(course.course_description, response_data[0])
