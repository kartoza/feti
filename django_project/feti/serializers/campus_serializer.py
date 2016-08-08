__author__ = 'irwan'

from rest_framework import serializers
from feti.models.campus import Campus


class CampusSerializer(serializers.ModelSerializer):
    class Meta:
        model = Campus
