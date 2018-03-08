# coding=utf-8
"""A command to update FieldSubfieldOfStudy which integrate subfield of study
    with field of study.
"""
from django.core.management.base import BaseCommand
from feti.models.course import Course
from feti.models.field_subfield_of_study import FieldSubfieldOfStudy


class Command(BaseCommand):
    help = 'Update FieldSubfieldOfStudy from courses'

    def handle(self, *args, **options):
        courses = Course.objects.all()
        for course in courses:
            print('-------------------------------------')
            if course.field_of_study:
                field_subfield, created = FieldSubfieldOfStudy.objects.get_or_create(
                        field_of_study=course.field_of_study
                )
                print('Field of study %s' % field_subfield.field_of_study.field_of_study_description)
            if course.subfield_of_study:
                print('Subfield of study %s' % field_subfield.subfield_of_study.name)
                field_subfield.subfield_of_study.add(
                        course.subfield_of_study
                )
            print('-------------------------------------')
