from rest_framework.response import Response
from rest_framework.views import APIView

from feti.models.course_provider_link import (
    CourseProviderLink
)
from feti.serializers.course_provider_link import (
    CourseProviderLinkSerializer
)

__author__ = 'Alison Mukoma <alison@kartoza.com>'
__date__ = '22/10/17'
__license__ = "GPL"
__copyright__ = 'kartoza.com'


class CourseProviderLinkApiView(APIView):
    """
    Api to list all the course provider links.
    """

    def get(self, request):
        links = CourseProviderLink.objects.all()

        serializer = CourseProviderLinkSerializer(links, many=True)
        return Response(serializer.data)

