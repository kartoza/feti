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
        if request.GET.get('fos'):
            options['fos'] = request.GET.get('fos')
        if request.GET.get('sos'):
            options['sos'] = request.GET.get('sos')
        if request.GET.get('qt'):
            options['qt'] = request.GET.get('qt')
        if request.GET.get('mc'):
            options['mc'] = request.GET.get('mc')
        if request.GET.get('nqf'):
            options['nqf'] = request.GET.get('nqf')
        if request.GET.get('nqsf'):
            options['nqsf'] = request.GET.get('nqsf')

        if 'fos' or 'sos' or 'qt' or 'mc' or 'nqf' or 'nqsf' in options:
            options['advance_search'] = True

        return query, options

    def filter_indexed_campus(self, query):
        """
        Filter using campus index model.
        :param sqs: Search Query Set
        :return: filtered sqs
        """
        sqs = SearchQuerySet().filter(
            long_description=query,
            campus_location_is_null='false',
            courses_is_null='false'
        ).models(Campus)
        return sqs

    def filter_by_course(self, query):
        sqs = SearchQuerySet().filter(
            course_course_description=query,
            campus_location_isnull='false',
        ).models(CampusCourseEntry)
        return sqs

    def filter_indexed_campus_course(self, query):
        sqs = SearchQuerySet().filter(
            campus_and_provider=query,
            campus_location_isnull='false'
        ).models(CampusCourseEntry)
        return sqs

    def filter_fos(self, sqs, fos):
        """

        :param sqs: Search Query Set
        :param fos: Field of study
        :return:
        """
        return sqs.filter(
            field_of_study_id=Exact(fos)
        ).models(CampusCourseEntry)

    def filter_sos(self, sqs, sos):
        """

        :param sqs: Search Query Set
        :param sos: Subfield of study
        :return:
        """
        return sqs.filter(
            subfield_of_study_id=Exact(sos)
        ).models(CampusCourseEntry)

    def filter_qualification_type(self, sqs, qt):
        """

        :param sqs:
        :param qt: qualitifaction type
        :return:
        """
        return sqs.filter(
            qualification_type_id=Exact(qt)
        ).models(CampusCourseEntry)

    def filter_minimum_credits(self, sqs, mc):
        """

        :param sqs:
        :param mc: minimum credits
        :return:
        """
        return sqs.filter(
            minimum_credits=Exact(mc)
        ).models(CampusCourseEntry)

    def filter_nqf(self, sqs, nqf):
        """

        :param sqs:
        :param nqf: National Qualifications Framework
        :return:
        """
        return sqs.filter(
            national_qualifications_framework_id=Exact(nqf)
        ).models(CampusCourseEntry)

    def filter_nqsf(self, sqs, nqsf):
        """

        :param sqs:
        :param nqsf: National Qualifications Subframework
        :return:
        """
        return sqs.filter(
            national_qualifications_subframework_id=Exact(nqsf)
        ).models(CampusCourseEntry)

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
