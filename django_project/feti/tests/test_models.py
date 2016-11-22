# coding=utf-8
"""Module related to test for all the models."""
from unittest.mock import patch
from django.test import TestCase
from feti.tests.model_factories import (
    CampusFactory,
    AddressFactory,
    ProviderFactory,
    CourseFactory,
    EducationTrainingQualityAssuranceFactory
)


class TestCampusCRUD(TestCase):
    """
    Tests Campus models.
    """

    def setUp(self):
        """
        Sets up before each test
        """
        self.course = CourseFactory.create()
        self.course.save()
        self.course2 = CourseFactory.create()

    @patch('feti.celery.update_search_index.delay')
    def test_Campus_create(self, mock):
        """
        Tests Campus model creation
        """
        model = CampusFactory.create(courses=(self.course, self.course2))

        # check if signal triggered
        self.assertTrue(mock.called)

        # check if PK exists
        self.assertTrue(model.id is not None)

        # check if name exists
        self.assertTrue(model.campus is not None)

    @patch('feti.celery.update_search_index.delay')
    def test_Campus_read(self, mock):
        """
        Tests Campus model read
        """
        model = CampusFactory.create(
            campus=u'Custom Campus',
            courses=(self.course,)
        )

        # check if signal triggered
        self.assertTrue(mock.called)

        self.assertTrue(model.campus == 'Custom Campus')

    @patch('feti.celery.update_search_index.delay')
    def test_Campus_update(self, mock):
        """
        Tests Campus model update
        """
        model = CampusFactory.create(courses=(self.course,))
        new_model_data = {
            'campus': u'New Campus Name',
        }
        model.__dict__.update(new_model_data)
        model.save()

        # check if signal triggered
        self.assertTrue(mock.called)

        # check if updated
        for key, val in new_model_data.items():
            self.assertEqual(model.__dict__.get(key), val)

    @patch('feti.celery.update_search_index.delay')
    def test_Campus_delete(self, mock):
        """
        Tests Campus model delete
        """
        model = CampusFactory.create(courses=(self.course,))

        # check if signal triggered
        self.assertTrue(mock.called)

        model.delete()

        # check if deleted
        self.assertTrue(model.id is None)


class TestCourseCRUD(TestCase):
    """
    Tests Course models.
    """

    def setUp(self):
        """
        Sets up before each test
        """
        pass

    def test_Course_create(self):
        """
        Tests Course model creation
        """
        model = CourseFactory.create()

        # check if PK exists
        self.assertTrue(model.id is not None)

        # check if course_description exists
        self.assertTrue(model.course_description is not None)

        self.assertTrue(model.education_training_quality_assurance is not None)

    def test_Course_read(self):
        """
        Tests Course model read
        """
        model = CourseFactory.create(
            course_description=u'Custom Course'
        )

        self.assertTrue(model.course_description == 'Custom Course')

    def test_Course_update(self):
        """
        Tests Course model update
        """
        model = CourseFactory.create()
        education = EducationTrainingQualityAssuranceFactory.create()
        new_model_data = {
            'course_description': u'Course description',
            'education_training_quality_assurance': education
        }
        model.__dict__.update(new_model_data)
        model.save()

        # check if updated
        for key, val in new_model_data.items():
            self.assertEqual(model.__dict__.get(key), val)

    def test_Course_delete(self):
        """
        Tests Course model delete
        """
        model = CourseFactory.create()

        model.delete()

        # check if deleted
        self.assertTrue(model.id is None)
