from rest_framework import serializers
from feti.models.national_qualification_framework_subframework import (
    NationalQualificationFrameworkSubFramework
)

__author__ = 'Dimas Ciputra <dimas@kartoza.com>'
__date__ = '13/02/17'
__license__ = "GPL"
__copyright__ = 'kartoza.com'


class NationalQualificationsSubFrameworkSerializer(serializers.ModelSerializer):

    class Meta:
        model = NationalQualificationFrameworkSubFramework
        fields = '__all__'
