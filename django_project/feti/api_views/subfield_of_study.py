from rest_framework.response import Response
from rest_framework.views import APIView

from feti.models.subfield_of_study import SubFieldOfStudy
from feti.models.field_subfield_of_study import FieldSubfieldOfStudy
from feti.serializers.subfield_of_study_serializer import SubFieldOfStudySerializer

__author__ = 'Dimas Ciputra <dimas@kartoza.com>'
__date__ = '13/02/17'
__license__ = "GPL"
__copyright__ = 'kartoza.com'


class SubFieldOfStudyAPIView(APIView):
    """
    Api to list all subfield of study.
    """
    def get(self, request):
        field = request.GET.get('field')
        if not field:
            subfield_of_study = SubFieldOfStudy.objects.order_by(
                    'learning_subfield'
            )
        else:
            try:
                field_subfield = FieldSubfieldOfStudy.objects.get(
                        field_of_study_id=field
                )
                subfield_of_study = field_subfield.subfield_of_study.order_by(
                        'learning_subfield'
                )
            except FieldSubfieldOfStudy.DoesNotExist:
                return Response([])

        serializer = SubFieldOfStudySerializer(subfield_of_study, many=True)
        return Response(serializer.data)
