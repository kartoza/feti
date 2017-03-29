from rest_framework import serializers
from feti.models.field_of_study import FieldOfStudy

__author__ = 'Dimas Ciputra <dimas@kartoza.com>'
__date__ = '13/02/17'
__license__ = "GPL"
__copyright__ = 'kartoza.com'


class FieldOfStudySerializer(serializers.ModelSerializer):

    class Meta:
        model = FieldOfStudy
        fields = '__all__'
