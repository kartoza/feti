from rest_framework.response import Response
from rest_framework.views import APIView

from feti.models.occupation import Occupation
from feti.serializers.occupation_serializer import OccupationListSerializer

__author__ = 'Alison Mukoma <alison@kartoza.com>'
__date__ = '24/10/17'
__license__ = "GPL"
__copyright__ = 'kartoza.com'


class OccupationListApiView(APIView):
    """
    Api to list all available occupations.
    """
    def get(self, request):
        occupations = Occupation.objects.only('occupation')

        serializer = OccupationListSerializer(occupations, many=True)
        return Response(serializer.data)
