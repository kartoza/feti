# coding=utf-8
"""Model factory definitions for models."""

import factory
from unittest.mock import MagicMock
from feti.models import (
    Campus,
    Address,
    Provider,
    Course,
    EducationTrainingQualityAssurance,
    NationalQualificationsFramework
)


class ProviderFactory(factory.DjangoModelFactory):
    """Factory class for provider model."""
    class Meta:
        model = Provider

    primary_institution = factory.Sequence(lambda n: 'primary institution %s' % n)
    website = u'Provider Website'


class AddressFactory(factory.DjangoModelFactory):
    """Factory class for address model."""
    class Meta:
        model = Address

    address_line_1 = factory.Sequence(lambda n: 'address %s' % n)


class CampusFactory(factory.DjangoModelFactory):
    """Factory class for Campus model."""
    class Meta:
        model = Campus

    campus = factory.Sequence(lambda n: 'Campus %s' % n)
    address = factory.SubFactory(AddressFactory)
    provider = factory.SubFactory(ProviderFactory)
    Campus.update_index = MagicMock(print('call update index'))

    @factory.post_generation
    def courses(self, create, extracted, **kwargs):
        if not create:
            # Simple build, do nothing.
            return

        if extracted:
            # A list of groups were passed in, use them
            for course in extracted:
                self.courses.add(course)


class EducationTrainingQualityAssuranceFactory(factory.DjangoModelFactory):
    """Factory for EducationTrainingQualityAssurance."""
    class Meta:
        model = EducationTrainingQualityAssurance

    acronym = factory.Sequence(lambda n: "Acronym%s" % n)
    body_name = factory.Sequence(lambda n: "Body name %s" % n)


class CourseFactory(factory.DjangoModelFactory):
    """Factory class for Course model."""
    class Meta:
        model = Course

    national_learners_records_database = factory.Sequence(lambda n: 'NLRD %s' % n)
    course_description = factory.Sequence(lambda n: 'course %s' % n)
    education_training_quality_assurance = factory.SubFactory(
        EducationTrainingQualityAssuranceFactory
    )
