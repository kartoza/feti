from rest_framework import serializers
from feti.models.campus import Campus

__author__ = 'irwan'


class CampusSerializer(serializers.ModelSerializer):
    class Meta:
        model = Campus
