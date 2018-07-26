from rest_framework.response import Response
from rest_framework.views import APIView

from feti.api_views.common_search import CommonSearch
from feti.models.campus import Campus
from feti.serializers.campus_serializer import CampusSummarySerializer


class ApiCampus(CommonSearch, APIView):
    """
    Api to filter campus by query
    """

    def get(self, request, *args):
        """Get the campuses.

        :param request: HTTP request object
        :type request: HttpRequest

        :param args: Positional arguments
        :type args: tuple
        
        :returns: URL
        :rtype: HttpResponse
        """

        query_dict = self.request.GET.dict()
        query, options = self.process_request(query_dict)
        campus_data = self.search_campuses(query, options)
        return Response(campus_data)


class CampusSummary(APIView):
    """Get detail of campus"""

    def get(self, request):
        campus_id = request.GET.get('id')

        if not campus_id:
            return Response(None)

        try:
            campus = Campus.objects.get(id=campus_id)
        except Campus.DoesNotExist:
            return Response(None)

        serializer = CampusSummarySerializer(campus)

        return Response(serializer.data)
