from django.core.management.base import BaseCommand

from feti.utils import get_soup
from feti.utilities.scraper.occupation_scraper import scrap_occupations

__author__ = 'Irwan Fathurrahman <irwan@kartoza.com>'
__date__ = '15/09/16'
__license__ = "GPL"
__copyright__ = 'kartoza.com'


class Command(BaseCommand):
    help = 'Scrapping the occupation information'
    args = '<args>'

    def add_arguments(self, parser):
        parser.add_argument(
            '--char',
            dest='char',
            help='Range of character to scrap from ncap list'
        )
        parser.add_argument(
            '--limitpage',
            dest='limitpage',
            help='Page limit'
        )

    def handle(self, *args, **options):
        scrap_occupations(char=options['char'], limitpage=options['limitpage'])
