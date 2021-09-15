
from rest_framework import serializers

class AppSerializer(serializers.Serializer):
    yeka = serializers.CharField()
    region = serializers.CharField()
    competition = serializers.CharField()
    company = serializers.CharField()
    uuid=serializers.UUIDField()


class AppResponseSerializer(serializers.Serializer):
    data = AppSerializer(many=True)
    draw = serializers.IntegerField()
    recordsTotal = serializers.IntegerField()
    recordsFiltered = serializers.IntegerField()