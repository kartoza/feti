from rest_framework.response import Response
from rest_framework.views import APIView

from feti.models.qual_class import QualClass

from feti.serializers.qual_class_serializer import QualClassSerializer

__author__ = 'Alison Mukoma <alison@kartoza.com>'
__date__ = '22/10/17'
__license__ = "GPL"
__copyright__ = 'kartoza.com'


class QualClassApiView(APIView):
    """
    Api to list all the titles of the Qualification Class.
    """

    def get(self, request):
        qual_class = QualClass.objects.all()

        serializer = QualClassSerializer(qual_class, many=True)
        return Response(serializer.data)

