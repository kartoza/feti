from rest_framework import serializers
from feti.models.learning_pathway import StepDetail

__author__ = 'irwan'


class StepDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = StepDetail

    def to_representation(self, instance):
        res = super(StepDetailSerializer, self).to_representation(instance)
        return res
