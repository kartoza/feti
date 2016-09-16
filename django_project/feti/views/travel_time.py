__author__ = 'Christian Christelis <christian@kartoza.com>'
__date__ = '16/09/16'

from rest_framework.views import APIView
from feti.utilities.utilities import get_travel_time
from rest_framework.response import Response


class TravelTime(APIView):
    response_type = 'text'

    def get(self, request, origin, destination):
        return Response(
            get_travel_time(origin, destination, self.response_type))

