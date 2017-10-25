from rest_framework.response import Response
from rest_framework.views import APIView

from feti.models.abet_band import AbetBand

from feti.serializers.abet_band_serializer import AbetBandSerializer

__author__ = 'Alison Mukoma <alison@kartoza.com>'
__date__ = '22/10/17'
__license__ = "GPL"
__copyright__ = 'kartoza.com'


class AbetBandApiView(APIView):
    """
    Api to list all Abet Bands.
    """

    def get(self, request):
        bands = AbetBand.objects.all()

        serializer = AbetBandSerializer(bands, many=True)
        return Response(serializer.data)


