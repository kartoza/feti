from rest_framework.response import Response
from rest_framework.views import APIView

from feti.models.education_training_quality_assurance import (
    EducationTrainingQualityAssurance
)

from feti.serializers.education_training_quality_assurance_serializer import (
    EducationTrainingQualityAssuranceSerializer
)

__author__ = 'Alison Mukoma <alison@kartoza.com>'
__date__ = '22/10/17'
__license__ = "GPL"
__copyright__ = 'kartoza.com'


class EducationTrainingQualityAssuranceApiView(APIView):
    """
    Api to list all the contents of Education
    Training Quality Assurance.
    """

    def get(self, request):
        model_data = EducationTrainingQualityAssurance.objects.all()

        serializer = EducationTrainingQualityAssuranceSerializer(model_data, many=True)
        return Response(serializer.data)

