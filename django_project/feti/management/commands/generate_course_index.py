# coding=utf-8
"""FETI landing page view."""

import os
from django.conf import settings
from django.core.management.base import BaseCommand

from feti.models.course import Course

__author__ = 'Irwan Fathurrahman <irwan@kartoza.com>'
__date__ = '07/09/16'
__license__ = "GPL"
__copyright__ = 'kartoza.com'


class Command(BaseCommand):
    def handle(self, *args, **options):
        # check the folder
        if not os.path.exists(settings.CACHE_DIR):
            os.makedirs(settings.CACHE_DIR)

        print("generate courses index start")
        # write course_strings cache
        filename = os.path.join(
            settings.CACHE_DIR,
            'course_strings')

        # get data
        courses = Course.objects.all().order_by('course_description')
        courses_names = [
            course.course_description.strip() for course in courses
            if course.course_description]
        courses_names = list(set(courses_names))
        courses_names.sort()
        courses_names = "\n".join(courses_names)

        # safe to file
        file = open(filename, 'w', encoding='utf-8')
        file.write(courses_names)  # python will convert \n to os.linesep
        file.close()  # you can omit in most cases as the destructor will call it
        print("generate courses index finish")
