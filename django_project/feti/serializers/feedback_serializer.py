from __future__ import absolute_import
from rest_framework import serializers
from feti.models.feedback import Feedback

__author__ = 'Alison Mukoma <alison@kartoza.com>'
__date__ = '19/10/17'
__license__ = "GPL"
__copyright__ = 'kartoza.com'


class FeedbackSerializer(serializers.ModelSerializer):
    """Adds a serializer for Feedback model."""

    class Meta:
        model = Feedback
        fields = '__all__'
