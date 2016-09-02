import json

from django.db.models import Q
from django.contrib.gis.geos import Polygon
from rest_framework.response import Response
from rest_framework.views import APIView

from feti.models.campus import Campus
from feti.models.course import Course
from feti.serializers.campus_serializer import CampusSerializer
from feti.serializers.course_serializer import CourseSerializer

__author__ = 'Irwan Fathurrahman <irwan@kartoza.com>'
__date__ = '08/08/16'
__license__ = "GPL"
__copyright__ = 'kartoza.com'


class ApiCampus(APIView):
    def get(self, request, format=None):
        q = request.GET.get('q')
        coord_string = request.GET.get('coord')
        drawn_polygon = {}

        if coord_string:
            coord_obj = json.loads(coord_string)
            poly = []
            for c in coord_obj:
                poly.append((c['lng'], c['lat']))
            poly.append(poly[0])
            drawn_polygon = Polygon(poly)

        if not q:
            q = ""
        if coord_string:
            campuses = Campus.objects.filter(
                Q(campus__icontains=q) |
                Q(provider__primary_institution__icontains=q),
                location__within=drawn_polygon
            )
        else:
            campuses = Campus.objects.filter(
                Q(campus__icontains=q) |
                Q(provider__primary_institution__icontains=q)
            )
        serializer = CampusSerializer(campuses, many=True)
        return Response(serializer.data)


class ApiCourse(APIView):
    def get(self, request, format=None):
        q = request.GET.get('q')
        if not q:
            q = ""

        set = Course.objects.filter(course_description__icontains=q)
        serializer = CourseSerializer(set, many=True)
        return Response(serializer.data)
