from django.core.management.base import BaseCommand

from feti.models.address import Address
from feti.models.campus import Campus
from feti.models.provider import Provider
from feti.utilities.scraper.campus_scraper import scrap_all_campuses

__author__ = 'Irwan Fathurrahman <irwan@kartoza.com>'
__date__ = '15/09/16'
__license__ = "GPL"
__copyright__ = 'kartoza.com'


class Command(BaseCommand):
    args = '<args>'
    help = 'This script is for scaping campus on website source. \n'
    true_words = ['true', 't', '1', 'y', 'yes']

    def add_arguments(self, parser):
        parser.add_argument(
            '--delete',
            dest='delete',
            default=False,
            help='Delete all address, campus, provider',
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
            Address.objects.all().delete()
            Campus.objects.all().delete()
            Provider.objects.all().delete()

        from_page = 0
        to_page = 0
        if options['from_page']:
            from_page = options['from_page']

        if options['to_page']:
            to_page = options['to_page']

        scrap_all_campuses(start_page=from_page, max_page=to_page)
