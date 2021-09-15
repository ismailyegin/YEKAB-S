from rest_framework import serializers

from ekabis.models.ConnectionRegion import ConnectionRegion


class ConnectionRegionSerializer(serializers.ModelSerializer):
    class Meta:
        model = ConnectionRegion
        fields = '__all__'
        depth = 3