# -*- coding: utf-8 -*-
import abc
import os
import json
from django.db.models import Q
from django.core.serializers.json import DjangoJSONEncoder
from django.conf import settings
from django.contrib.gis.geos import Polygon, Point
from django.contrib.gis.measure import Distance
from django.http import HttpResponse, HttpResponseBadRequest
from rest_framework.response import Response
from rest_framework.views import APIView
from haystack.query import RelatedSearchQuerySet, SQ, SearchQuerySet
from haystack.inputs import Clean

from feti.models.campus import Campus
from feti.models.occupation import Occupation
from feti.models.campus_course_entry import CampusCourseEntry
from feti.serializers.campus_serializer import CampusSerializer
from feti.serializers.occupation_serializer import OccupationSerializer

from map_administrative.views import get_boundary

__author__ = 'Irwan Fathurrahman <irwan@kartoza.com>'
__date__ = '08/08/16'
__license__ = "GPL"
__copyright__ = 'kartoza.com'


class SearchCampus(APIView):
    additional_context = {}

    def get(self, request, format=None):
        query = request.GET.get('q')
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

        campuses = self.filter_model(query)

        if drawn_polygon:
            campuses = campuses.filter(
                    location__within=drawn_polygon
                )
        elif drawn_circle:
            campuses = campuses.filter(
                    location__distance_lt=(drawn_circle, Distance(m=radius))
                )

        user_campuses = []
        if self.request.user.is_authenticated():
            user_campuses = list(self.request.user.profile.campus_favorites.all().values_list('id', flat=True))

        self.additional_context['user_campuses'] = user_campuses

        serializer = CampusSerializer(campuses, many=True, context=self.additional_context)
        return Response(serializer.data)

    @abc.abstractmethod
    def additional_filter(self, model, query):
        return

    @abc.abstractmethod
    def filter_model(self, query):
        return


class ApiCampus(SearchCampus):
    def get(self, request, format=None):
        return SearchCampus.get(self, request)

    def filter_model(self, query):
        q = Clean(query)
        sqs = SearchQuerySet().filter(
                SQ(campus_campus=q) |
                SQ(campus_provider=q),
                campus_location_isnull='false',
                courses_isnull='false'
        ).models(CampusCourseEntry)
        campuses = Campus.objects.filter(id__in=set([x.object.campus.id for x in sqs]))
        # Get all courses
        self.additional_context['courses'] = None
        return campuses

    def additional_filter(self, model, query):
        return model.filter(
            Q(campus__icontains=query) |
            Q(provider__primary_institution__icontains=query))


class ApiCourse(SearchCampus):
    def get(self, request, format=None):
        return SearchCampus.get(self, request)

    def filter_model(self, query):
        sqs = SearchQuerySet().filter(
            course_course_description=query,
            campus_location_isnull='false',
        ).models(CampusCourseEntry)
        campuses = Campus.objects.filter(id__in=set([x.object.campus.id for x in sqs]))
        # Only shows this courses
        self.additional_context['courses'] = set([x.object.course_id for x in sqs])
        return campuses

    def additional_filter(self, model, query):
        return model.distinct().filter(
            courses__course_description__icontains=query
        )


class ApiOccupation(SearchCampus):
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

    def additional_filter(self, model, query):
        return model.distinct().filter(
            occupation__icontains=query
        )


class ApiSavedCampus(SearchCampus):
    def get(self, request, format=None):
        return SearchCampus.get(self, request)

    def filter_model(self, query):
        campuses = list(self.request.user.profile.campus_favorites.all())
        return campuses

    def additional_filter(self, model, query):
        pass


class ApiAutocomplete(APIView):

    def get(self, request, model):
        q = request.GET.get('q')
        q = q.lower()

        # read course_strings cache
        if model == 'provider':
            sqs = SearchQuerySet().filter(
                SQ(campus_campus=q) |
                SQ(campus_provider=q),
                campus_location_isnull='false',
                courses_isnull='false'
            ).models(CampusCourseEntry)[:10]
            suggestions = list(set([result.object.campus.campus if q in result.object.campus.campus.lower()
                           else result.object.campus.provider.primary_institution for result in sqs]))
        elif model == 'course':
            sqs = SearchQuerySet().autocomplete(course_course_description=q).models(CampusCourseEntry)[:10]
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

    def get_from_file(self, request, model):
        q = request.GET.get('q')
        q = q.lower()

        # check the folder
        if not os.path.exists(settings.CACHE_DIR):
            os.makedirs(settings.CACHE_DIR)

        # read course_strings cache
        if model == 'provider':
            filename = os.path.join(
                settings.CACHE_DIR,
                'campus_strings')
        elif model == 'course':
            filename = os.path.join(
                settings.CACHE_DIR,
                'course_strings')
        elif model == 'occupation':
            filename = os.path.join(
                settings.CACHE_DIR,
                'occupation_strings')
        else:
            return HttpResponse(
                json.dumps(
                    {'result': 'error',
                     'status_code': HttpResponseBadRequest.status_code},
                    cls=DjangoJSONEncoder),
                content_type='application/json')

        with open(filename, 'r', encoding='utf-8') as file:
            raw_list = file.readlines()

        exact_list = [string for string in raw_list if q == string.lower()[:len(q)]]
        containse_list = [string for string in raw_list
                          if q != string.lower()[:len(q)] and q in string.lower()]
        list = exact_list + containse_list

        return HttpResponse(
            json.dumps(list, cls=DjangoJSONEncoder),
            content_type='application/json')
