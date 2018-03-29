# coding: utf-8
__author__ = 'Alison Mukoma <alison@kartoza.com>'
__copyright__ = 'kartoza.com'

import time
from prometheus_client import Summary

# Create a metric to track time spent and requests made.
PAGE_REQUEST_TIME = Summary('get_view_response_time',
                            'Time the request took to respond.')


class ResponseTimeMixin(object):
    """Gets the response time a decorated function process took."""

    @PAGE_REQUEST_TIME.time()
    def get_response_time(self, request, *args, **kwargs):
        """Method to calculate the response-time for a request."""

        # start the timer
        request.start_time = time.time()

        # stop timer when object is done and return time value
        duration = int((time.time() - request.start_time) * 1000)
        # Add the header.
        return duration


# Create a metric to track time spent and requests made.
SYSTEM_RESOURCE_STATS = Summary('get_system_resource_statistics',
                            'System resource statistics.')

class ProcessGaugeDispatch(object):
    """Get system statistics where the project is running."""

