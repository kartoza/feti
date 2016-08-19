from rest_framework.response import Response
from rest_framework.views import APIView
from feti.models.campus import Campus
from feti.models.course import Course
from feti.models.campus_course_entry import CampusCourseEntry
from feti.serializers.campus_serializer import CampusSerializer
from feti.serializers.course_serializer import CourseSerializer

__author__ = 'Irwan Fathurrahman <irwan@kartoza.com>'
__date__ = '08/08/16'
__license__ = "GPL"
__copyright__ = 'kartoza.com'


class ApiCampuss(APIView):
    def get(self, request, format=None):
        set = Campus.objects.all()
        serializer = CampusSerializer(set, many=True)
        return Response(serializer.data)


class ApiCourses(APIView):
    def get(self, request, campus_id=None, format=None):
        set = CampusCourseEntry.objects.filter(campus=campus_id).values('course')
        set = Course.objects.filter(id__in=set)
        serializer = CourseSerializer(set, many=True)
        return Response(serializer.data)
