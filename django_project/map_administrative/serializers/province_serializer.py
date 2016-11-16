from rest_framework_gis.serializers import GeoFeatureModelSerializer, GeometrySerializerMethodField
from map_administrative.models.province import Province

__author__ = 'irwan'


class ProvinceSerializer(GeoFeatureModelSerializer):
    geometry = GeometrySerializerMethodField()

    def get_geometry(self, obj):
        return None

    class Meta:
        model = Province
        geo_field = 'polygon_geometry'
        fields = '__all__'

    def to_representation(self, instance):
        res = super(ProvinceSerializer, self).to_representation(instance)
        res['properties']['id'] = instance.id
        res['properties']['layer'] = 'province'
        res['properties']['title'] = instance.parent() + "," + instance.name
        res['properties']['color'] = '#f44a52'
        return res
