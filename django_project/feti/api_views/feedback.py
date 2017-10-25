from rest_framework.response import Response
from rest_framework.views import APIView

from feti.models.feedback import Feedback

from feti.serializers.feedback_serializer import FeedbackSerializer

__author__ = 'Alison Mukoma <alison@kartoza.com>'
__date__ = '22/10/17'
__license__ = "GPL"
__copyright__ = 'kartoza.com'


class FeedbackApiView(APIView):
    """
    Api to list all the contents of feedback.
    """

    def get(self, request):
        feedback = Feedback.objects.all()

        serializer = FeedbackSerializer(feedback, many=True)
        return Response(serializer.data)

