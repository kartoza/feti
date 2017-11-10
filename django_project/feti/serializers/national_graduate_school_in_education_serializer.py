from rest_framework import serializers
from feti.models.national_graduate_school_in_education import (
    NationalGraduateSchoolInEducation
)
__author__ = 'Alison Mukoma <alison@kartoza.com>'
__date__ = '19/10/17'
__license__ = "GPL"
__copyright__ = 'kartoza.com'


class NationalGraduateSchoolInEducationSerializer(serializers.ModelSerializer):
    """
    Adds a serializer for
    NationalGraduateSchoolInEducation model.
    """

    class Meta:
        model = NationalGraduateSchoolInEducation
        fields = '__all__'
