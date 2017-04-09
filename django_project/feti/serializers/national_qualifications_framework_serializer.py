from rest_framework import serializers
from feti.models.national_qualifications_framework import NationalQualificationsFramework

__author__ = 'Dimas Ciputra <dimas@kartoza.com>'
__date__ = '13/02/17'
__license__ = "GPL"
__copyright__ = 'kartoza.com'


class NationalQualificationsFrameworkSerializer(serializers.ModelSerializer):

    id = serializers.SerializerMethodField('get_nqf_id')
    text = serializers.SerializerMethodField('get_nqf_text')

    def get_nqf_id(self, obj):
        return obj.level

    def get_nqf_text(self, obj):
        return 'NQF Level %s' % obj.level

    class Meta:
        model = NationalQualificationsFramework
        fields = '__all__'
