from __future__ import absolute_import

from rest_framework import serializers
from feti.models.course_provider_link import CourseProviderLink

__author__ = 'Alison Mukoma <alison@kartoza.com>'
__date__ = '19/10/17'
__license__ = "GPL"
__copyright__ = 'kartoza.com'

class CourseProviderLinkSerializer(serializers.ModelSerializer):
    """Serializes CourseProviderLink model."""

    class Meta:
        model = CourseProviderLink
        field = '__all__'