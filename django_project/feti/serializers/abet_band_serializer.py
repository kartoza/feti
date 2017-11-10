from __future__ import absolute_import

from rest_framework import serializers
from feti.models.abet_band import AbetBand

__author__ = 'Alison Mukoma <alison@kartoza.com>'
__date__ = '19/10/17'
__license__ = "GPL"
__copyright__ = 'kartoza.com'

class AbetBandSerializer(serializers.ModelSerializer):
    """Adds model serializer for AbetBand."""

    class Meta:
        model = AbetBand
        fields = '__all__'
