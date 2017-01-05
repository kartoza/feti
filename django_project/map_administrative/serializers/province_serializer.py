from rest_framework_gis.serializers import GeoFeatureModelSerializer, GeometrySerializerMethodField
from map_administrative.models.province import Province
from rest_framework import serializers

__author__ = 'irwan'


class ProvinceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Province
        exclude = ('country',)

    def to_representation(self, instance):
        res = super(ProvinceSerializer, self).to_representation(instance)
        res['id'] = instance.id
        res['layer'] = 'province'
        res['title'] = instance.name
        res['color'] = '#f44a52'
        return res
