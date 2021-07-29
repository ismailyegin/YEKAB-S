from rest_framework import serializers

from ekabis.models.Company import Company


class CompanySerializer(serializers.ModelSerializer):
    class Meta:
        model = Company
        fields = '__all__'
        depth = 4


class CompanyResponseSerializer(serializers.Serializer):
    data = CompanySerializer(many=True)
    draw = serializers.IntegerField()
    recordsTotal = serializers.IntegerField()
    recordsFiltered = serializers.IntegerField()
