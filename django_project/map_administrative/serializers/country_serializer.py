from rest_framework_gis.serializers import GeoFeatureModelSerializer, GeometrySerializerMethodField
from map_administrative.models.country import Country
from rest_framework import serializers

__author__ = 'irwan'


class CountrySerializer(serializers.ModelSerializer):
    class Meta:
        model = Country
        fields = '__all__'

    def to_representation(self, instance):
        res = super(CountrySerializer, self).to_representation(instance)
        res['id'] = instance.id
        res['layer'] = 'country'
        res['title'] = instance.name
        res['color'] = '#f44a52'
        return res
