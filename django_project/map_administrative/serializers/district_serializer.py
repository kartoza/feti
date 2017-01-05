from rest_framework_gis.serializers import GeoFeatureModelSerializer, GeometrySerializerMethodField
from map_administrative.models.district import District
from rest_framework import serializers

__author__ = 'Dimas Ciputra <dimas@kartoza.com>'
__revision__ = '$Format:%H$'
__date__ = '20/12/16'


class DistrictSerializer(serializers.ModelSerializer):
    """Serializer for District model."""

    class Meta:
        model = District
        fields = '__all__'

    def to_representation(self, instance):
        res = super(DistrictSerializer, self).to_representation(instance)
        res['id'] = instance.id
        res['layer'] = 'district'
        res['title'] = instance.parent() + "," + instance.name
        res['color'] = '#4AF497'
        return res
