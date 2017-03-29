from rest_framework import serializers
from feti.models.qualification_type import QualificationType

__author__ = 'Dimas Ciputra <dimas@kartoza.com>'
__date__ = '13/02/17'
__license__ = "GPL"
__copyright__ = 'kartoza.com'


class QualificationTypeSerializer(serializers.ModelSerializer):

    class Meta:
        model = QualificationType
        fields = '__all__'
