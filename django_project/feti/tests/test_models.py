# coding=utf-8
"""Module related to test for all the models."""
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
        pass

    def test_Campus_create(self):
        """
        Tests Campus model creation
        """
        model = CampusFactory.create()

        # check if PK exists
        self.assertTrue(model.id is not None)

        # check if name exists
        self.assertTrue(model.campus is not None)

    def test_Campus_read(self):
        """
        Tests Campus model read
        """
        model = CampusFactory.create(
            campus=u'Custom Campus'
        )

        self.assertTrue(model.campus == 'Custom Campus')

    def test_Campus_update(self):
        """
        Tests Campus model update
        """
        model = CampusFactory.create()
        new_model_data = {
            'campus': u'New Campus Name'
        }
        model.__dict__.update(new_model_data)
        model.save()

        # check if updated
        for key, val in new_model_data.items():
            self.assertEqual(model.__dict__.get(key), val)

    def test_Campus_delete(self):
        """
        Tests Campus model delete
        """
        model = CampusFactory.create()

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
