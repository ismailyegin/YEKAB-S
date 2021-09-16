from rest_framework import serializers

from ekabis.models.CompetitionApplication import CompetitionApplication


class YekaApplicationSerializer(serializers.ModelSerializer):
    class Meta:
        model = CompetitionApplication
        fields = '__all__'
        depth = 3