from rest_framework.response import Response
from rest_framework.views import APIView

from feti.models.national_graduate_school_in_education import (
    NationalGraduateSchoolInEducation
)

from feti.serializers.national_graduate_school_in_education_serializer import (
    NationalGraduateSchoolInEducationSerializer
)

__author__ = 'Alison Mukoma <alison@kartoza.com>'
__date__ = '22/10/17'
__license__ = "GPL"
__copyright__ = 'kartoza.com'


class NationalGraduateSchoolInEducationApiView(APIView):
    """
    Api to list all the contents of feedback.
    """

    def get(self, request):
        ngsie = NationalGraduateSchoolInEducation.objects.all()

        serializer = NationalGraduateSchoolInEducationSerializer\
            (ngsie, many=True)
        return Response(serializer.data)

