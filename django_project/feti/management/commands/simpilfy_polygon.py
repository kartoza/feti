__author__ = 'Irwan Fathurrahman <irwan@kartoza.com>'
__date__ = '12/01/17'

from django.core.management.base import BaseCommand
from map_administrative.models.country import Country
from map_administrative.models.district import District
from map_administrative.models.municipality import Municipality
from map_administrative.models.province import Province

from map_administrative.utilities.utilities import simplify_polygon_geometry_of_boundary


class Command(BaseCommand):
    help = '''Simplify administrative polygon.
    This command will simplify polygon for administrative
    with tolerance for the Douglas-Peucker algorithm is 0.001.

    There is --administratives options, to filter which administrative
    will be simplify.

    Example : python manage.py simplify_polygon "Country,District"

    WARNING:
    THIS WILL SIMPLIFY POLYGON. IF YOU RUN THIS AGAIN, IT WILL SIMPLIFY AGAIN AND
    COULD BE RESULT IN BAD POLYGON
    '''

    def add_arguments(self, parser):
        # Named (optional) arguments
        parser.add_argument(
            '--administratives',
            dest='administratives',
            help='administrative models that will be checked',
        )

    def handle(self, *args, **options):
        administratives = [Country, Province, District, Municipality]
        if options['administratives']:
            administratives = []
            for administrative in options['administratives'].split(','):
                administrative = administrative.lower()
                Boundary = None
                if administrative == 'country':
                    Boundary = Country
                elif administrative == 'district':
                    Boundary = District
                elif administrative == 'municipality':
                    Boundary = Municipality
                elif administrative == 'province':
                    Boundary = Province
                administratives.append(Boundary)

        # simplify it
        for Boundary in administratives:
            simplify_polygon_geometry_of_boundary(Boundary)
