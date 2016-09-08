# -*- coding: utf-8 -*-
import abc
import os
import json
from django.db.models import Q
from django.core.serializers.json import DjangoJSONEncoder
from django.conf import settings
from django.contrib.gis.geos import Polygon
from django.http import HttpResponse, HttpResponseBadRequest
from rest_framework.response import Response
from rest_framework.views import APIView

from feti.models.campus import Campus
from feti.serializers.campus_serializer import CampusSerializer

__author__ = 'Irwan Fathurrahman <irwan@kartoza.com>'
__date__ = '08/08/16'
__license__ = "GPL"
__copyright__ = 'kartoza.com'


class SearchCampus(APIView):
    def get(self, request, format=None):
        query = request.GET.get('q')
        if len(query) < 3:
            return Response([])

        # Get coordinates from request and create a polygon
        coord_string = request.GET.get('coord')
        drawn_polygon = None
        if coord_string:
            coord_obj = json.loads(coord_string)
            poly = []
            for c in coord_obj:
                poly.append((c['lng'], c['lat']))
            poly.append(poly[0])
            drawn_polygon = Polygon(poly)

        if not query:
            query = ""

        campuses = Campus.objects.filter(location__isnull=False)
        campuses = self.additional_filter(campuses, query)

        if drawn_polygon:
            campuses = campuses.filter(
                location__within=drawn_polygon
            )

        campuses.order_by('campus')
        serializer = CampusSerializer(campuses, many=True)
        return Response(serializer.data)

    @abc.abstractmethod
    def additional_filter(self, model):
        return


class ApiCampus(SearchCampus):
    def get(self, request, format=None):
        return SearchCampus.get(self, request)

    def additional_filter(self, model, query):
        return model.filter(Q(campus__icontains=query) | Q(provider__primary_institution__icontains=query))


class ApiCourse(SearchCampus):
    def get(self, request, format=None):
        return SearchCampus.get(self, request)

    def additional_filter(self, model, query):
        return model.distinct().filter(
            courses__course_description__icontains=query
        )


class ApiAutocomplete(APIView):
    def get(self, request, model):
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
        else:
            return HttpResponse(
                json.dumps(
                    {'result': 'error',
                     'status_code': HttpResponseBadRequest.status_code},
                    cls=DjangoJSONEncoder),
                content_type='application/json')

        raw_list = []
        with open(filename, 'r', encoding='utf-8') as file:
            raw_list = file.readlines()

        exact_list = [string for string in raw_list if q == string.lower()[:len(q)]]
        containse_list = [string for string in raw_list
                          if q != string.lower()[:len(q)] and q in string.lower()]
        list = exact_list + containse_list

        return HttpResponse(
            json.dumps(list, cls=DjangoJSONEncoder),
            content_type='application/json')
