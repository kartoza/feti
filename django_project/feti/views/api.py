# -*- coding: utf-8 -*-
import abc
import json
from itertools import chain
from more_itertools import unique_everseen
from django.db.models import Q
from django.core.serializers.json import DjangoJSONEncoder
from django.contrib.gis.geos import Polygon
from django.contrib.gis.measure import Distance
from django.http import HttpResponse, HttpResponseBadRequest
from django.core.exceptions import MultipleObjectsReturned
from rest_framework.response import Response
from rest_framework.views import APIView
from haystack.query import SQ, SearchQuerySet
from haystack.inputs import Clean
from haystack.utils.geo import Point, D

from feti.models.campus_course_entry import CampusCourseEntry
from feti.serializers.campus_serializer import CampusSerializer
from feti.serializers.occupation_serializer import OccupationSerializer
from feti.serializers.favorite_serializer import FavoriteSerializer
from user_profile.models import CampusCoursesFavorite

from map_administrative.views import get_boundary

__author__ = 'Irwan Fathurrahman <irwan@kartoza.com>'
__date__ = '08/08/16'
__license__ = "GPL"
__copyright__ = 'kartoza.com'


class SearchCampus(APIView):
    additional_context = {}
    courses_name = []

    def get(self, request, format=None):

        self.additional_context['courses'] = None

        query = request.GET.get('q')
        if query and len(query) < 3:
            return Response([])
        self.additional_context['query'] = query

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
            campuses = self.filter_model(
                query=query,
                options={
                    'type': 'polygon',
                    'shape': drawn_polygon
                }
            )
        elif drawn_circle:
            campuses = self.filter_model(
                query=query,
                options={
                    'type': 'circle',
                    'shape': drawn_circle,
                    'radius': radius
                }
            )
        else:
            campuses = self.filter_model(query)

        if not campuses:
            return Response('')

        if self.request.user.is_authenticated():
            campus_courses_favorite = list(CampusCoursesFavorite.objects.filter(
                user=self.request.user,
                campus__in=campuses))
            if campus_courses_favorite:
                self.additional_context['campus_saved'] = campus_courses_favorite

        serializer = CampusSerializer(campuses, many=True, context=self.additional_context)
        return Response(serializer.data)

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
                            p
                        )
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

    @abc.abstractmethod
    def additional_filter(self, model, query):
        return

    @abc.abstractmethod
    def filter_model(self, query, options=None):
        return


class ApiCampus(SearchCampus):
    """
    Api to filter campus by query
    """
    def get(self, request, format=None):
        return SearchCampus.get(self, request)

    def filter_model(self, query, options=None):
        campuses = None
        q = Clean(query)
        sqs = SearchQuerySet()
        sqs = sqs.filter(
            SQ(campus_campus=q) | SQ(campus_provider=q),
            campus_location_isnull='false',
            courses_isnull='false'
        )

        if options and 'shape' in options:
            if options['type'] == 'polygon':
                sqs = self.filter_polygon(sqs, options['shape'])
            elif options['type'] == 'circle':
                sqs = self.filter_radius(
                        sqs,
                        options['shape'],
                        options['radius']
                )

        if sqs:
            campuses = list(unique_everseen([x.object.campus for x in sqs]))
        return campuses

    def additional_filter(self, model, query):
        return model.filter(
            Q(campus__icontains=query) |
            Q(provider__primary_institution__icontains=query))


class ApiCourse(SearchCampus):
    """
    Api to filter courses by query
    """

    def get(self, request, format=None):
        return SearchCampus.get(self, request)

    def filter_model(self, query, options=None):
        sqs = None
        campuses = None

        if '=' in query:
            queries = query.split('=')
            # search by saqa id
            if 'saqa_id' in queries[0] and len(queries) > 1:
                saqa_ids = queries[1].split(',')
                try:
                    sqs = SearchQuerySet().filter(
                        course_nlrd__in=saqa_ids
                    ).models(CampusCourseEntry)
                except MultipleObjectsReturned as e:
                    print(e)

        if not sqs:
            sqs = SearchQuerySet().filter(
                course_course_description=query,
                campus_location_isnull='false',
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

        if sqs:
            campuses = list(unique_everseen([x.object.campus for x in sqs]))
            # Only shows this courses
            self.additional_context['courses'] = list(unique_everseen([x.object.course_id for x in sqs]))

        return campuses


class ApiOccupation(APIView):
    def get(self, request, format=None):
        query = request.GET.get('q')
        if len(query) < 3:
            return Response([])

        occupation = self.filter_model(query)

        serializer = OccupationSerializer([x.object for x in occupation], many=True)
        return Response(serializer.data)

    def filter_model(self, query):
        sqs = SearchQuerySet().filter(
            occupation__icontains=Clean(query)
        )
        return sqs


class ApiSavedCampus(APIView):

    def get(self, request, format=None):
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

        campus_course_fav = CampusCoursesFavorite.objects.filter(
            user=self.request.user)

        if drawn_polygon:
            campus_course_fav = campus_course_fav.filter(
                    campus__location__within=drawn_polygon
                )
        elif drawn_circle:
            campus_course_fav = campus_course_fav.filter(
                    campus__location__distance_lt=(drawn_circle, Distance(m=radius))
                )

        serializer = FavoriteSerializer(campus_course_fav, many=True)
        return Response(serializer.data)


class ApiAutocomplete(APIView):

    def get(self, request, model):
        q = request.GET.get('q')
        q = q.lower()

        # read course_strings cache
        if model == 'provider':
            sqs1 = SearchQuerySet().filter(
                campus_campus=q,
                campus_location_isnull='false',
                courses_isnull='false'
            ).models(CampusCourseEntry)[:5]
            sqs2 = SearchQuerySet().filter(
                campus_provider=q,
                campus_location_isnull='false',
                courses_isnull='false'
            ).models(CampusCourseEntry)[:5]
            sqs = list(chain(sqs1, sqs2))
            suggestions = list(set([result.object.campus.campus if q in result.object.campus.campus.lower()
                           else result.object.campus.provider.primary_institution for result in sqs]))
        elif model == 'course':
            sqs = SearchQuerySet().autocomplete(
                    course_course_description=q
            ).models(CampusCourseEntry)[:10]
            suggestions = list(set([result.course_course_description for result in sqs]))
        elif model == 'occupation':
            api = ApiOccupation()
            sqs = api.filter_model(query=q)
            suggestions = [result.occupation for result in sqs]
        else:
            return HttpResponse(
                json.dumps(
                    {'result': 'error',
                     'status_code': HttpResponseBadRequest.status_code},
                    cls=DjangoJSONEncoder),
                content_type='application/json')

        return HttpResponse(
            json.dumps(suggestions, cls=DjangoJSONEncoder),
            content_type='application/json')
