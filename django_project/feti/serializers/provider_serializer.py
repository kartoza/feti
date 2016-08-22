from rest_framework import serializers
from feti.models.provider import Provider

__author__ = 'irwan'


class ProviderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Provider
