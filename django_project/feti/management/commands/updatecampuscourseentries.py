# coding=utf-8
from feti.models.campus import Campus
from feti.models.campus_course_entry import CampusCourseEntry
from feti.models.course import Course

__author__ = 'Rizky Maulana Nugraha "lucernae" <lana.pcfre@gmail.com>'
__date__ = '16/07/15'


from django.core.management.base import BaseCommand, CommandError


class Command(BaseCommand):
    help = 'Update long description in Campus and Course models'

    def handle(self, *args, **options):
        self.stdout.write('Updating Campus Course Entries...')
        entries_added = 0
        entries_deleted = 0
        for campus in Campus.objects.all():
            courses = campus.courses.all()
            course_ids = [c.id for c in courses]
            entries = []
            # bulk add courses entries
            for c in courses:
                try:
                    CampusCourseEntry.objects.get(campus=campus, course=c)
                except CampusCourseEntry.DoesNotExist:
                    entries.append(CampusCourseEntry(campus=campus, course=c))

            CampusCourseEntry.objects.bulk_create(entries)
            entries_added += len(entries)

            # bulk delete courses entries
            campus_course_entries = CampusCourseEntry.objects.filter(
                campus=campus)
            for entry in campus_course_entries:
                if entry.course.id not in course_ids:
                    entry.delete()
                    entries_deleted += 1

        self.stdout.write('Update completed.')
        self.stdout.write('Entries added : %d' % entries_added)
        self.stdout.write('Entries deleted : %d' % entries_deleted)
