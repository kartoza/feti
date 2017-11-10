from rest_framework import serializers
from feti.models.education_training_quality_assurance import (
    EducationTrainingQualityAssurance
)

__author__ = 'Alison Mukoma <alison@kartoza.com>'
__date__ = '19/10/17'
__license__ = "GPL"
__copyright__ = 'kartoza.com'


class EducationTrainingQualityAssuranceSerializer(serializers.ModelSerializer):
    """Adds a serializer for Feedback model."""

    class Meta:
        model = EducationTrainingQualityAssurance
        fields = '__all__'
