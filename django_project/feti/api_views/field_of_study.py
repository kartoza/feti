from rest_framework.response import Response
from rest_framework.views import APIView

from feti.models.field_of_study import FieldOfStudy
from feti.serializers.field_of_study_serializer import FieldOfStudySerializer

__author__ = 'Dimas Ciputra <dimas@kartoza.com>'
__date__ = '13/02/17'
__license__ = "GPL"
__copyright__ = 'kartoza.com'


class FieldOfStudyAPIView(APIView):
    """
    Api to list all field of study.
    """
    def get(self, request):
        field_of_study = FieldOfStudy.objects.order_by('field_of_study_description')

        serializer = FieldOfStudySerializer(field_of_study, many=True)
        return Response(serializer.data)
