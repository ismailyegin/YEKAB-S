from rest_framework import serializers

from ekabis.models.Yeka import Yeka


class YekaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Yeka
        fields = '__all__'
        depth = 4


class YekaResponseSerializer(serializers.Serializer):
    data = YekaSerializer(many=True)
    draw = serializers.IntegerField()
    recordsTotal = serializers.IntegerField()
    recordsFiltered = serializers.IntegerField()
