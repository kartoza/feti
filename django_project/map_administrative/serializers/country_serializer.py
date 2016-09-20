from rest_framework_gis.serializers import GeoFeatureModelSerializer, GeometrySerializerMethodField
from map_administrative.models.country import Country

__author__ = 'irwan'


class CountrySerializer(GeoFeatureModelSerializer):
    geometry = GeometrySerializerMethodField()

    def get_geometry(self, obj):
        return None

    class Meta:
        model = Country
        geo_field = 'polygon_geometry'

    def to_representation(self, instance):
        res = super(CountrySerializer, self).to_representation(instance)
        res['properties']['id'] = instance.id
        res['properties']['layer'] = 'country'
        res['properties']['title'] = instance.name
        res['properties']['color'] = '#f44a52'
        return res
