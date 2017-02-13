import json
from rest_framework.response import Response
from haystack.utils.geo import Point, D
from haystack.query import SearchQuerySet
from haystack.inputs import Clean, Exact
from django.contrib.gis.geos import Polygon

from map_administrative.views import get_boundary
from feti.models.campus import Campus
from feti.models.campus_course_entry import CampusCourseEntry

__author__ = 'Irwan Fathurrahman <irwan@kartoza.com>'
__date__ = '08/08/16'
__license__ = "GPL"
__copyright__ = 'kartoza.com'


class CampusSearch(object):

    def process_request(self, request):
        """Process get request from site.
        """

        query = request.GET.get('q')
        options = dict()

        if query and len(query) < 3:
            return Response([])

        # Get coordinates from request and create a polygon
        shape = request.GET.get('shape')
        drawn_polygon = None
        drawn_circle = None
        radius = 0

        if shape == 'polygon':
            coord_string = request.GET.get('coordinates')
            if coord_string:
                coord_obj = json.loads(coord_string)
                poly = []
                for c in coord_obj:
                    poly.append((c['lng'], c['lat']))
                poly.append(poly[0])
                drawn_polygon = Polygon(poly)
        elif shape == 'circle':
            coord_string = request.GET.get('coordinate')
            radius = request.GET.get('radius')
            if coord_string:
                coord_obj = json.loads(coord_string)
                drawn_circle = Point(coord_obj['lng'], coord_obj['lat'])

        boundary = get_boundary(request.GET.get('administrative'))
        if boundary:
            drawn_polygon = boundary.polygon_geometry

        # Advance search
        field_of_study = request.GET.get('fos')

        if not query:
            query = ""

        if drawn_polygon:
            options = {
                'type': 'polygon',
                'shape': drawn_polygon
            }
        elif drawn_circle:
            options = {
                'type': 'circle',
                'shape': drawn_circle,
                'radius': radius
            }

        if field_of_study:
            options['fos'] = field_of_study

        return query, options

    def filter_indexed_campus(self, query):
        """
        Filter search query set by query
        :param sqs: Search Query Set
        :return: filtered sqs
        """
        sqs = SearchQuerySet().filter(
                long_description=query,
                campus_location_is_null='false',
                courses_is_null='false'
        ).models(Campus)
        return sqs

    def filter_campus_with_fos(self, query, fos=None):
        if fos:
            sqs = SearchQuerySet().filter(
                campus_and_provider=query,
                campus_location_isnull='false',
                field_of_study_id=Exact(fos)
            ).models(CampusCourseEntry)
        else:
            sqs = SearchQuerySet().filter(
                campus_and_provider=query,
                campus_location_isnull='false'
            ).models(CampusCourseEntry)
        return sqs

    def filter_polygon(self, sqs, polygon):
        """
        Filter search query set by polygon
        :param sqs: Search Query Set
        :return: filtered sqs
        """
        # Check if multipolygon
        if polygon.geom_type == 'MultiPolygon':
            for p in polygon:
                sqs = sqs.polygon(
                        'campus_location',
                        p)
                if len(sqs) > 0:
                    return sqs
            return None
        else:
            return sqs.polygon(
                'campus_location',
                polygon
            )

    def filter_radius(self, sqs, point, radius):
        """
        Filter search query set by radius
        :param sqs: Search Query Set
        :return: filtered sqs
        """
        max_dist = D(m=radius)
        return sqs.dwithin(
            'campus_location',
            point,
            max_dist
        )
