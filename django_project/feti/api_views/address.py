from rest_framework.response import Response
from rest_framework.views import APIView

from feti.models.address import Address

from feti.serializers.address_serializer import AddressSerializer

__author__ = 'Alison Mukoma <alison@kartoza.com>'
__date__ = '22/10/17'
__license__ = "GPL"
__copyright__ = 'kartoza.com'


class AddressApiView(APIView):
    """
    Api to list all the Addresses.
    """

    def get(self, request):
        addresses = Address.objects.all()

        serializer = AddressSerializer(addresses, many=True)
        return Response(serializer.data)


