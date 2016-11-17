from rest_framework import serializers
from feti.models.provider import Provider
from feti.models.campus import Campus
from feti.serializers.campus_serializer import CampusSerializer

__author__ = 'irwan'


class ProviderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Provider
        fields = '__all__'

    def to_representation(self, instance):
        res = super(ProviderSerializer, self).to_representation(instance)
        campus = Campus.objects.filter(provider=instance)
        res['campus'] = CampusSerializer(campus, many=True).data
        return res
