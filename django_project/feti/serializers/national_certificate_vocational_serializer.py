from __future__ import absolute_import
from rest_framework import serializers
from feti.models.national_certificate_vocational import (
    NationalCertificateVocational
)

__author__ = 'Alison Mukoma <alison@kartoza.com>'
__date__ = '19/10/17'
__license__ = "GPL"
__copyright__ = 'kartoza.com'


class NationalCertificateVocationalSerializer(serializers.ModelSerializer):
    """
    Adds a serializer for
    NationalCertificateVocational model.
    """

    class Meta:
        model = NationalCertificateVocational
        fields = '__all__'
