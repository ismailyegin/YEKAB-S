from rest_framework import serializers

from ekabis.models.Employee import Employee


class EmployeeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Employee
        fields = '__all__'
        depth = 4


class EmployeeResponseSerializer(serializers.Serializer):
    data = EmployeeSerializer(many=True)
    draw = serializers.IntegerField()
    recordsTotal = serializers.IntegerField()
    recordsFiltered = serializers.IntegerField()
