from rest_framework import serializers
from feti.models.occupation import Occupation
from feti.models.learning_pathway import LearningPathway, Step
from feti.serializers.step_detail_serializer import StepDetailSerializer

__author__ = 'irwan'


class OccupationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Occupation
        fields = '__all__'

    def to_representation(self, instance):
        res = super(OccupationSerializer, self).to_representation(instance)
        res['title'] = instance.__unicode__()
        res['model'] = 'occupation'
        # get pathway
        res['pathways'] = {}

        learning_pathways = LearningPathway.objects.filter(
            occupation=instance
        ).order_by(
            'pathway_number'
        )

        for pathway in learning_pathways:
            res['pathways'][pathway.pathway_number] = {}
            for step in Step.objects.filter(
                    learning_pathway=pathway
            ).order_by(
                'step_number'
            ):
                detail = step.step_detail
                res['pathways'][pathway.pathway_number][step.step_number] = \
                    StepDetailSerializer(detail).data
        return res


class OccupationListSerializer(serializers.ModelSerializer):
    """
    API to list all the available occupations.
    """
    class Meta:
        model = Occupation
        fields = '__all__'
