# -*- coding: utf-8 -*-
import abc
import json
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.core.serializers.json import DjangoJSONEncoder
from django.conf import settings
from django.contrib.gis.geos import Polygon
from django.contrib.gis.measure import Distance
from django.db.models import Q
from django.http import HttpResponse, HttpResponseBadRequest

from rest_framework.response import Response
from rest_framework.views import APIView
from haystack.query import SQ, SearchQuerySet
from haystack.inputs import Clean, Exact
from haystack.utils.geo import Point, D

from feti.models.campus_course_entry import CampusCourseEntry
from feti.serializers.occupation_serializer import OccupationSerializer
from feti.serializers.favorite_serializer import FavoriteSerializer
from user_profile.models import CampusCoursesFavorite
from feti.models.campus import Campus

from map_administrative.views import get_boundary

__author__ = 'Irwan Fathurrahman <irwan@kartoza.com>'
__date__ = '08/08/16'
__license__ = "GPL"
__copyright__ = 'kartoza.com'


class SearchCampus(APIView):
    page_limit = settings.LIMIT_PER_PAGE
    additional_context = {}
    courses_name = []

    def get(self, request, format=None):

        self.additional_context['courses'] = None

        query = request.GET.get('q')
        if query and len(query) < 3:
            return Response([])
        self.additional_context['query'] = query
        self.page = request.GET.get('page', 0)

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

        return Response(campuses)

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
        q = Clean(query)
        if query:
            q = Clean(query)
            sqs = SearchQuerySet()
            sqs = sqs.filter(
                long_description=q,
                campus_location_is_null='false',
                courses_is_null='false'
            ).models(Campus)
        else:
            sqs = SearchQuerySet()
            sqs = sqs.filter(
                campus_location_is_null='false',
                courses_is_null='false'
            ).models(Campus)

        if options and 'shape' in options:
            if options['type'] == 'polygon':
                sqs = self.filter_polygon(
                    sqs,
                    options['shape']
                )
            elif options['type'] == 'circle':
                sqs = self.filter_radius(
                    sqs,
                    options['shape'],
                    options['radius']
                )

        paginator = Paginator(sqs, self.page_limit)
        try:
            sqs = paginator.page(self.page)
        except PageNotAnInteger:
            page = 1
            sqs = paginator.page(page)
        except EmptyPage:
            page = paginator.num_pages
            sqs = paginator.page(page)

        campus_data = []

        if sqs:
            for result in sqs:
                stored_fields = result.get_stored_fields()
                if stored_fields['campus_location']:
                    campus_location = stored_fields['campus_location']
                    stored_fields['campus_location'] = "{0},{1}".format(
                        campus_location.y, campus_location.x
                    )

                del stored_fields['courses_is_null']
                del stored_fields['campus_is_null']
                del stored_fields['campus_location_is_null']
                del stored_fields['courses_id']
                del stored_fields['provider_primary_institution']
                del stored_fields['campus_auto']
                del stored_fields['long_description']
                del stored_fields['text']
                del stored_fields['campus_popup']

                campus_data.append(stored_fields)

        return campus_data

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

    def filter_by_saqa_ids(self, saqa_ids, options=None):
        # Filter by exact value of saqa id

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

    def filter_model(self, query, options=None):

        if '=' in query:
            queries = query.split('=')
            # search by saqa id
            if 'saqa_id' in queries[0] and len(queries) > 1:
                saqa_ids = queries[1].split(',')
                return self.filter_by_saqa_ids(saqa_ids, options)

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

        campus_data = []

        if sqs:
            for result in sqs:
                stored_fields = result.get_stored_fields()
                if stored_fields['campus_location']:
                    campus_location = stored_fields['campus_location']
                    stored_fields['campus_location'] = "{0},{1}".format(
                        campus_location.y, campus_location.x
                    )
                campus_data.append(stored_fields)

        return campus_data


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
    def filter_model(self, user, options=None, query=None):
        drawn_polygon = None
        drawn_circle = None
        shape = None
        administrative = None
        radius = 0

        if options:
            if 'shape' in options:
                shape = options['shape']
            if 'administrative' in options:
                administrative = get_boundary(options['administrative'])

        if shape and shape == 'polygon':
            coord_string = options['coordinates']
            if coord_string:
                coord_obj = json.loads(coord_string)
                poly = []
                for c in coord_obj:
                    poly.append((c['lng'], c['lat']))
                poly.append(poly[0])
                drawn_polygon = Polygon(poly)
        elif shape and shape == 'circle':
            coord_string = options['coordinates']
            radius = options['radius']

            if coord_string:
                coord_obj = json.loads(coord_string)
                drawn_circle = Point(coord_obj['lng'], coord_obj['lat'])

        if administrative:
            boundary = get_boundary(administrative)
            if boundary:
                drawn_polygon = boundary.polygon_geometry

        campus_course_fav = CampusCoursesFavorite.objects.filter(
            user=user)

        if drawn_polygon:
            campus_course_fav = campus_course_fav.filter(
                campus__location__within=drawn_polygon
            )
        elif drawn_circle:
            campus_course_fav = campus_course_fav.filter(
                campus__location__distance_lt=(drawn_circle, Distance(m=radius))
            )

        return campus_course_fav

    def get(self, request, format=None):
        if not self.request.user.is_authenticated():
            return HttpResponse('Unauthorized', status=401)

        # Get coordinates from request and create a polygon
        shape = request.GET.get('shape')
        options = dict()

        if shape:
            options['shape'] = shape
        if shape == 'polygon':
            options['coordinates'] = request.GET.get('coordinates')
        elif shape == 'circle':
            options['coordinates'] = request.GET.get('coordinate')
            options['radius'] = request.GET.get('radius')
        administrative = request.GET.get('administrative')
        if administrative:
            options['administrative'] = administrative

        favorites = self.filter_model(user=self.request.user, options=options)

        serializer = FavoriteSerializer(favorites, many=True)
        return Response(serializer.data)


class ApiAutocomplete(APIView):
    def get(self, request, model):
        q = request.GET.get('q')
        q = q.lower()

        # read course_strings cache
        if model == 'provider':
            sqs = SearchQuerySet().autocomplete(
                long_description=q,
                campus_location_is_null='false',
                courses_is_null='false'
            ).models(Campus)[:10]
            suggestions = list(set([result.campus if q in result.object.campus.lower()
                                    else result.campus_provider for result in sqs]))
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
