from rest_framework import serializers

from ekabis.models import Neighborhood


class NeighborhoodSerializer(serializers.ModelSerializer):
    class Meta:
        model = Neighborhood
        fields = '__all__'
        depth = 3
