from rest_framework import serializers
from feti.models.qual_class import QualClass

__author__ = 'Alison Mukoma <alison@kartoza.com>'
__date__ = '19/10/17'
__license__ = "GPL"
__copyright__ = 'kartoza.com'


class QualClassSerializer(serializers.ModelSerializer):
    """Adds a serializer for QualClass Model."""

    class Meta:
        model = QualClass
        fields = '__all__'
