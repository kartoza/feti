__author__ = 'Christian Christelis <christian@kartoza.com>'
__date__ = '16/09/16'


from django.views.generic import View

from feti.utilities.utilities import get_travel_time

class TravelTime(View):
    response_type = 'text'

    def get(self, request, origin, destination):
        return get_travel_time(origin, destination, self.response_type)
