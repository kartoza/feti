# coding=utf-8
"""FETI landing page view."""

import os
from django.conf import settings
from django.core.management.base import BaseCommand

from feti.models.occupation import Occupation

__author__ = 'Irwan Fathurrahman <irwan@kartoza.com>'
__date__ = '07/09/16'
__license__ = "GPL"
__copyright__ = 'kartoza.com'


class Command(BaseCommand):
    def handle(self, *args, **options):
        # check the folder
        if not os.path.exists(settings.CACHE_DIR):
            os.makedirs(settings.CACHE_DIR)

        print("generate occupations index start")
        # write course_strings cache
        filename = os.path.join(
            settings.CACHE_DIR,
            'occupation_strings')

        # get data
        occupations = Occupation.objects.all().order_by('occupation')
        occupation_names = [
            occupation.occupation for occupation in occupations]
        occupation_names = list(set(occupation_names))
        occupation_names.sort()
        occupation_names = "\n".join(occupation_names)

        # safe to file
        file = open(filename, 'w', encoding='utf-8')
        file.write(occupation_names)  # python will convert \n to os.linesep
        file.close()  # you can omit in most cases as the destructor will call it
        print("generate occupations index finish")
