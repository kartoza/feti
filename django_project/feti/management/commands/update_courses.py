# coding=utf-8
"""A command to update courses data, the new data will be fetch from saqa site"""
from django.core.management.base import BaseCommand
from django.db.utils import IntegrityError as dbIntegrityError
from psycopg2 import IntegrityError
from feti.models.course import Course
from feti.models.campus import Campus
from feti.management.commands.scraping_course import get_course_detail_from_saqa


class Command(BaseCommand):
    """
    Update all courses to saqa equivalents and remove duplicates course
    """
    args = ''
    # noinspection PyShadowBuiltins
    help = 'Update all courses from local database'

    def add_arguments(self, parser):
        parser.add_argument(
            '--id',
            dest='id',
            help='Qualification id'
        )

    def handle(self, *args, **options):
        """
        Implementation for command
        :param args: Not used
        :param options: qualification id
        """
        if options['id']:
            courses = Course.objects.filter(national_learners_records_database=options['id'])
        else:
            courses = Course.objects.all()

        for course in courses:
            if course.national_learners_records_database:
                print('-----------------------------------------------')
                print('Processing {} - {}'.format(
                    course.national_learners_records_database,
                    course.course_description))
                # check duplicates
                duplicates = courses.filter(
                    national_learners_records_database=course.national_learners_records_database
                ).exclude(id=course.id)
                if len(duplicates) > 0:
                    print("Removing duplicates")
                    campuses = Campus.objects.filter(courses__in=duplicates)
                    for campus in campuses:
                        try:
                            campus.courses.add(course)
                        except (IntegrityError, dbIntegrityError) as e:
                            print(e)
                            break
                    duplicates.delete()

                print('Updating from saqa sites by qualification id')
                get_course_detail_from_saqa(course.national_learners_records_database, False)
