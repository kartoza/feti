# coding=utf-8
from feti.models.campus import Campus
from feti.models.course import Course
from django.core.management.base import BaseCommand

__author__ = 'Rizky Maulana Nugraha "lucernae" <lana.pcfre@gmail.com>'
__date__ = '16/07/15'


class Command(BaseCommand):
    help = 'Update long description in Campus and Course models'

    def handle(self, *args, **options):
        self.stdout.write('Updating long description for Campus...')
        for campus in Campus.objects.all():
            campus.save()
        self.stdout.write('Update completed.')
        self.stdout.write('---------------------------------------')
        self.stdout.write('Updating long description for Course...')
        for course in Course.objects.all():
            course.save()
        self.stdout.write('Update completed.')
