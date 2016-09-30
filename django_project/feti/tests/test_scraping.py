__author__ = 'Irwan Fathurrahman <irwan@kartoza.com>'
__date__ = '30/09/16'
__license__ = "GPL"
__copyright__ = 'kartoza.com'

from django.core.management import call_command
from django.test import TestCase
from feti.models.campus import Campus
from feti.models.course import Course
from feti.models.occupation import Occupation
from feti.models.provider import Provider


class TestScraping(TestCase):
    def get_campus_count(self):
        args = []
        opts = {}
        call_command('scraping_campus', *args, **opts)
        # check if name exists
        self.assertTrue(Campus.objects.all().count() >= 1)
        self.assertTrue(Provider.objects.all().count() >= 1)

    def get_course_count(self):
        args = []
        opts = {}
        call_command('scraping_course', *args, **opts)
        self.assertTrue(Course.objects.all().count() >= 1)

    def get_occupation_count(self):
        " Test scraping Occupation command."
        args = []
        opts = {}
        call_command('scraping_occupation', *args, **opts)
        self.assertTrue(Occupation.objects.all().count() >= 1)
