from rest_framework.response import Response
from rest_framework.views import APIView

from feti.models.national_certificate_vocational import (
    NationalCertificateVocational
)

from feti.serializers.national_certificate_vocational_serializer import (
    NationalCertificateVocationalSerializer
)

__author__ = 'Alison Mukoma <alison@kartoza.com>'
__date__ = '22/10/17'
__license__ = "GPL"
__copyright__ = 'kartoza.com'


class NationalCertificateVocationalApiView(APIView):
    """
    Api to list all the National
    Certificate Vocational Training Centers.
    """

    def get(self, request):
        ncv = NationalCertificateVocational.objects.all()

        serializer = NationalCertificateVocationalSerializer(ncv, many=True)
        return Response(serializer.data)

