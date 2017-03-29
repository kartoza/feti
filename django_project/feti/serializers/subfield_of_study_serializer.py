from rest_framework import serializers
from feti.models.subfield_of_study import SubFieldOfStudy

__author__ = 'Dimas Ciputra <dimas@kartoza.com>'
__date__ = '13/02/17'
__license__ = "GPL"
__copyright__ = 'kartoza.com'


class SubFieldOfStudySerializer(serializers.ModelSerializer):

    class Meta:
        model = SubFieldOfStudy
        fields = '__all__'
