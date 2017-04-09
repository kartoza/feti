from rest_framework.response import Response
from rest_framework.views import APIView

from feti.models.national_qualifications_framework import NationalQualificationsFramework
from feti.serializers.national_qualifications_framework_serializer import (
    NationalQualificationsFrameworkSerializer
)

__author__ = 'Dimas Ciputra <dimas@kartoza.com>'
__date__ = '13/02/17'
__license__ = "GPL"
__copyright__ = 'kartoza.com'


class NationalQualificationsFrameworkAPIView(APIView):
    """
    Api to list all national qualifications framework.
    """
    def get(self, request):
        national_qualifications_framework = NationalQualificationsFramework.objects.order_by('level')

        serializer = NationalQualificationsFrameworkSerializer(
                national_qualifications_framework,
                many=True)
        return Response(serializer.data)
