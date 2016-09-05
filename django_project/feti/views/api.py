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

        if not q:
            q = ""

        campuses = Campus.objects.filter(location__isnull=False)
        campuses = campuses.filter(
            Q(campus__icontains=q) |
            Q(provider__primary_institution__icontains=q))

        if drawn_polygon:
            campuses = campuses.filter(
                location__within=drawn_polygon
            )

        campuses.order_by('campus')
        serializer = CampusSerializer(campuses, many=True)
        print(serializer.data)
        return Response(serializer.data)


class ApiCourse(APIView):
    def get(self, request, format=None):
        q = request.GET.get('q')

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

        if not q:
            q = ""

        campuses = Campus.objects.filter(location__isnull=False)
        campuses = campuses.filter(
            courses__course_description__icontains=q
        )

        if drawn_polygon:
            campuses = campuses.filter(
                location__within=drawn_polygon
            )

        campuses.order_by('campus')
        serializer = CampusSerializer(campuses, many=True)
        return Response(serializer.data)
