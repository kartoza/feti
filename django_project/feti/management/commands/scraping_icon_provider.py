from django.core.management.base import BaseCommand

from feti.utilities.scraper.campus_scraper import scrap_icons

__author__ = 'Irwan Fathurrahman <irwan@kartoza.com>'
__date__ = '15/09/16'
__license__ = "GPL"
__copyright__ = 'kartoza.com'


class Command(BaseCommand):
    help = 'Scrapping icon for provider'
    args = '<args>'
    true_words = ['true', 't', '1', 'y', 'yes']

    def add_arguments(self, parser):
        parser.add_argument(
            '--delete',
            dest='delete',
            default=False,
            help='Delete current icon',
        )

    def handle(self, *args, **options):
        delete = options['delete']
        if delete and delete in self.true_words:
            delete = True
        else:
            delete = False
        scrap_icons(replace=delete)
