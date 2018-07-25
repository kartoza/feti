import json
from rest_framework.response import Response
from haystack.utils.geo import Point, D
from haystack.query import SearchQuerySet
from haystack.inputs import Clean, Exact
from django.contrib.gis.geos import Polygon
from django.conf import settings

from map_administrative.views import get_boundary
from feti.models.campus import Campus
from feti.models.campus_course_entry import CampusCourseEntry

__author__ = 'Irwan Fathurrahman <irwan@kartoza.com>'
__date__ = '08/08/16'
__license__ = "GPL"
__copyright__ = 'kartoza.com'


class CommonSearch(object):
    page_limit = settings.LIMIT_PER_PAGE

    def process_request(self, request_dict):
        """Process get request from site.
        """

        query = None

        if 'query' in request_dict:
            query = request_dict.pop('query')
        elif 'q' in request_dict:
            query = request_dict.pop('q')

        options = dict()

        if query and len(query) < 3:
            return Response([])

        # Get coordinates from request and create a polygon
        shape = request_dict.pop('shape', None)
        drawn_polygon = None
        drawn_circle = None
        radius = 0

        if shape == 'polygon':
            coord_string = request_dict.pop('coordinates', None)
            if coord_string:
                coord_obj = json.loads(coord_string)
                poly = []
                for c in coord_obj:
                    poly.append((c['lng'], c['lat']))
                poly.append(poly[0])
                drawn_polygon = Polygon(poly)
        elif shape == 'circle':
            coord_string = request_dict.pop('coordinate', None)
            radius = request_dict.pop('radius', None)
            if coord_string:
                coord_obj = json.loads(coord_string)
                drawn_circle = Point(coord_obj['lng'], coord_obj['lat'])

        boundary = get_boundary(request_dict.pop('administrative', None))
        if boundary:
            drawn_polygon = boundary.polygon_geometry

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

        # Advance search
        advance_search_fields = [
            'fos',  # Field of study
            'sos',  # Subfield of study
            'qt',  # Qualification type
            'mc',  # Minimum credits
            'nqf',  # National qualification framework
            'nqsf',  # National qualifications subframework
            'pi'  # Public institution
        ]
        options.update(request_dict)

        if any(field for field in advance_search_fields if field in request_dict):
            options['advance_search'] = True
        else:
            options['advance_search'] = False

        page = request_dict.pop('page', None)
        options['page'] = page
        return query, options

    def filter_indexed_campus(self, query):
        """
        Filter using campus index model.
        :param sqs: Search Query Set
        :return: filtered sqs
        """
        if query:
            sqs = SearchQuerySet().filter(
                long_description=query,
                campus_location_is_null='false',
                courses_is_null='false'
            ).models(Campus)
        else:
            sqs = SearchQuerySet().filter(
                campus_location_is_null='false',
                courses_is_null='false'
            ).models(Campus)
        return sqs

    def filter_by_course(self, query):
        """Filter by course description
        :param query: Course query
        """
        if not query:
            sqs = SearchQuerySet().filter(
                    campus_location_isnull='false',
                    courses_isnull='false',
            ).models(CampusCourseEntry)
        else:
            sqs = SearchQuerySet().filter(
                course_course_description=query,
                campus_location_isnull='false',
            ).models(CampusCourseEntry)
        return sqs

    def filter_indexed_campus_course(self, query):
        """Filter by campus description
        :param query: Campus query
        """
        if query:
            sqs = SearchQuerySet().filter(
                campus_and_provider=query,
                campus_location_isnull='false'
            ).models(CampusCourseEntry)
        else:
            sqs = SearchQuerySet().filter(
                campus_location_isnull='false',
                courses_isnull='false',
            ).models(CampusCourseEntry)
        return sqs

    def filter_fos(self, sqs, fos):
        """Filter by field of study id.

        :param sqs: Search Query Set
        :param fos: Field of study
        :return:
        """
        return sqs.filter(
            field_of_study_id=Exact(fos)
        ).models(CampusCourseEntry)

    def filter_sos(self, sqs, sos):
        """Filter of subfield of study id.

        :param sqs: Search Query Set
        :param sos: Subfield of study
        :return:
        """
        return sqs.filter(
            subfield_of_study_id=Exact(sos)
        ).models(CampusCourseEntry)

    def filter_qualification_type(self, sqs, qt):
        """Filter by qualification type id.

        :param sqs: Search Query Set
        :param qt: qualitifaction type
        :return:
        """
        return sqs.filter(
            qualification_type_id=Exact(qt)
        ).models(CampusCourseEntry)

    def filter_minimum_credits(self, sqs, mc):
        """Filter by minimum credits

        :param sqs: Search Query Set
        :param mc: minimum credits
        :return:
        """
        return sqs.filter(
            minimum_credits__gte=mc
        ).models(CampusCourseEntry)

    def filter_nqf(self, sqs, nqf):
        """Filter by national qualification framework id

        :param sqs: Search Query Set
        :param nqf: National Qualifications Framework id
        :return:
        """
        return sqs.filter(
            national_qualifications_framework_id=Exact(nqf)
        ).models(CampusCourseEntry)

    def filter_nqsf(self, sqs, nqsf):
        """Filter by National Qualifications Subframework id

        :param sqs: Search Query Set
        :param nqsf: National Qualifications Subframework
        :return:
        """
        return sqs.filter(
            national_qualifications_subframework_id=Exact(nqsf)
        ).models(CampusCourseEntry)

    def filter_public_institution(self, sqs, pi):
        """Filter by public institution

        :param sqs: Search Query Set
        :param pi: Public institution ( true/false )
        :return:
        """
        return sqs.filter(
            campus_public_institution=pi
        ).models(CampusCourseEntry)

    def advanced_filter(self, sqs, options):
        """Advanced filter

        :param options: Additional query option
        :return:
        """
        if options and 'advance_search' in options:
            if 'fos' in options:
                sqs = self.filter_fos(sqs, options['fos'])
            if 'sos' in options:
                sqs = self.filter_sos(sqs, options['sos'])
            if 'qt' in options:
                sqs = self.filter_qualification_type(sqs, options['qt'])
            if 'mc' in options:
                sqs = self.filter_minimum_credits(sqs, options['mc'])
            if 'nqf' in options:
                sqs = self.filter_nqf(sqs, options['nqf'])
            if 'nqsf' in options:
                sqs = self.filter_nqsf(sqs, options['nqsf'])
            if 'pi' in options:
                sqs = self.filter_public_institution(sqs, options['pi'])
        return sqs

    def filter_by_saqa_ids(self, saqa_ids, options=None):
        """
        Filter by saqa id
        :param saqa_ids: List of saqa id
        :param options: Additional query option
        :return:
        """
        results = []

        if not saqa_ids:
            return results

        for saqa_id in saqa_ids:
            sqs = SearchQuerySet().filter(
                course_nlrd=Exact(saqa_id)
            ).models(CampusCourseEntry)
            if options and 'shape' in options:
                if options['type'] == 'polygon':
                    sqs = self.filter_polygon(sqs, options['shape'])
                elif options['type'] == 'circle':
                    sqs = self.filter_radius(
                        sqs,
                        options['shape'],
                        options['radius']
                    )

            if not sqs:
                continue

            sqs = self.advanced_filter(sqs, options)

            for result in sqs:
                stored_fields = result.get_stored_fields()
                if stored_fields['campus_location']:
                    campus_location = stored_fields['campus_location']
                    stored_fields['campus_location'] = "{0},{1}".format(
                        campus_location.y, campus_location.x
                    )
                    results.append(stored_fields)

        return results

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
