from rest_framework import serializers
from feti.models.address import Address

__author__ = 'irwan'


class AddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = Address
        fields = '__all__'
