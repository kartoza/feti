from map_administrative.models.municipality import Municipality
from rest_framework import serializers

__author__ = 'Dimas Ciputra <dimas@kartoza.com>'
__revision__ = '$Format:%H$'
__date__ = '05/01/17'


class MunicipalitySerializer(serializers.ModelSerializer):
    """Serializer for Municipality model."""

    class Meta:
        model = Municipality
        exclude = ('district',)

    def to_representation(self, instance):
        res = super(MunicipalitySerializer, self).to_representation(instance)
        res['id'] = instance.id
        res['layer'] = 'municipality'
        res['title'] = instance.parent() + "," + instance.name
        res['color'] = '#4AF497'
        return res
