from rest_framework.response import Response
from rest_framework.views import APIView

from feti.models.national_qualification_framework_subframework import (
    NationalQualificationFrameworkSubFramework
)
from feti.serializers.national_qualifications_subframework_serializer import (
    NationalQualificationsSubFrameworkSerializer
)

__author__ = 'Dimas Ciputra <dimas@kartoza.com>'
__date__ = '13/02/17'
__license__ = "GPL"
__copyright__ = 'kartoza.com'


class NationalQualificationsSubFrameworkAPIView(APIView):
    """
    Api to list all national qualifications framework.
    """
    def get(self, request):
        national_qualifications_framework = NationalQualificationFrameworkSubFramework.objects.all()

        serializer = NationalQualificationsSubFrameworkSerializer(
                national_qualifications_framework,
                many=True)
        return Response(serializer.data)
