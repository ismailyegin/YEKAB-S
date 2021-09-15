from rest_framework import serializers

from ekabis.models.YekaCompany import YekaCompany


class YekaCompanySerializer(serializers.ModelSerializer):
    class Meta:
        model = YekaCompany
        fields = '__all__'
        depth = 3



class YekaCompanyResponseSerializer(serializers.Serializer):
    data = YekaCompanySerializer(many=True)
    draw = serializers.IntegerField()
    recordsTotal = serializers.IntegerField()
    recordsFiltered = serializers.IntegerField()