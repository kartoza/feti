from django.core.management.base import BaseCommand
from feti.models.course import Course
from feti.utilities.scraper.course_scraper import get_course_detail_from_saqa, scraping_course_ncap

__author__ = 'Irwan Fathurrahman <irwan@kartoza.com>'
__date__ = '15/09/16'
__license__ = "GPL"
__copyright__ = 'kartoza.com'


class Command(BaseCommand):
    help = 'Scrapping the courses information'
    args = '<args>'

    def add_arguments(self, parser):
        parser.add_argument(
            '--id',
            dest='id',
            help='Qualification id'
        )
        parser.add_argument(
            '--re_cache',
            dest='re_cache',
            help='Update html cache'
        )
        parser.add_argument(
            '--no_cache',
            dest='no_cache',
            help='Do not use cached html'
        )
        parser.add_argument(
            '--delete',
            dest='delete',
            default=False,
            help='Delete all course',
        )
        parser.add_argument(
            '--from_page',
            dest='from_page',
            default=1,
            help='From page to be scraped',
        )
        parser.add_argument(
            '--to_page',
            dest='to_page',
            default=1,
            help='To page to be scraped',
        )

    def handle(self, *args, **options):
        if options['delete']:
            Course.objects.all().delete()

        if options['id']:
            no_cache = True if options['no_cache'] else False
            get_course_detail_from_saqa(options['id'], no_cache)
        else:

            from_page = 0
            to_page = 0
            if options['from_page']:
                from_page = options['from_page']

            if options['to_page']:
                to_page = options['to_page']

            scraping_course_ncap(start_page=from_page, max_page=to_page)
