from rest_framework.response import Response
from rest_framework.views import APIView

from feti.models.qualification_type import QualificationType
from feti.serializers.qualification_type_serializer import QualificationTypeSerializer

__author__ = 'Dimas Ciputra <dimas@kartoza.com>'
__date__ = '13/02/17'
__license__ = "GPL"
__copyright__ = 'kartoza.com'


class QualificationTypeAPIView(APIView):
    """
    Api to list all qualification type.
    """
    def get(self, request):
        qualification_type = QualificationType.objects.order_by('type')

        serializer = QualificationTypeSerializer(qualification_type, many=True)
        return Response(serializer.data)
