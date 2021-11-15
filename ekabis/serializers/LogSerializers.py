from rest_framework import serializers

from ekabis.models.Logs import Logs


class LogSerializer(serializers.ModelSerializer):
    class Meta:
        model = Logs
        fields = '__all__'
        depth = 3


class LogResponseSerializer(serializers.Serializer):
    data = LogSerializer(many=True)
    draw = serializers.IntegerField()
    recordsTotal = serializers.IntegerField()
    recordsFiltered = serializers.IntegerField()
