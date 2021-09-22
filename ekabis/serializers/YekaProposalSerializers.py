from rest_framework import serializers

from ekabis.models.Proposal import Proposal


class ProposalSerializer(serializers.ModelSerializer):
    class Meta:
        model = Proposal
        fields = '__all__'
        depth = 3