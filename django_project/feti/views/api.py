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
        if drawn_polygon:
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

        if drawn_polygon:
            # Get courses within the polygon area
            courses = Course.objects.distinct().filter(
                course_description__icontains=q,
                campus__location__within=drawn_polygon
            )
        else:
            courses = Course.objects.filter(
                course_description__icontains=q
            )

        serializer = CourseSerializer(
            courses,
            many=True,
            context={'drawn_polygon': drawn_polygon}
        )
        data = serializer.data

        return Response(data)
