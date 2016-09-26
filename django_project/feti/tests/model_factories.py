# coding=utf-8
"""Model factory definitions for models."""

import factory

from feti.models import (
    Campus,
    Address,
    Provider,
    Course,
    EducationTrainingQualityAssurance,
    NationalQualificationsFramework
)


class ProviderFactory(factory.Factory):
    """Factory class for provider model."""
    class Meta:
        model = Provider

    primary_institution = factory.Sequence(lambda n: 'primary institution %s' % n)
    website = u'Provider Website'


class AddressFactory(factory.Factory):
    """Factory class for address model."""
    class Meta:
        model = Address

    address_line_1 = factory.Sequence(lambda n: 'address %s' % n)
    campus_fk = factory.SubFactory('feti.tests.model_factories.CampusFactory')


class CampusFactory(factory.Factory):
    """Factory class for Campus model."""
    class Meta:
        model = Campus

    id = factory.Sequence(lambda n: n)
    campus = factory.Sequence(lambda n: 'Campus %s' % n)
    address = factory.SubFactory(AddressFactory)
    provider = factory.SubFactory(ProviderFactory)


class EducationTrainingQualityAssuranceFactory(factory.Factory):
    """Factory for EducationTrainingQualityAssurance."""
    class Meta:
        model = EducationTrainingQualityAssurance
    id = factory.Sequence(lambda n: n)
    acronym = factory.Sequence(lambda n: "Acronym%s" % n)
    body_name = factory.Sequence(lambda n: "Body name %s" % n)


class CourseFactory(factory.Factory):
    """Factory class for Course model."""
    class Meta:
        model = Course

    id = factory.Sequence(lambda n: n)
    national_learners_records_database = factory.Sequence(lambda n: 'NLRD %s' % n)
    course_description = factory.Sequence(lambda n: 'course %s' % n)
    education_training_quality_assurance = factory.SubFactory(
        EducationTrainingQualityAssuranceFactory
    )
