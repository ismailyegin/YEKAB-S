from rest_framework import serializers

from ekabis.models.YekaCompetitionEskalasyon import YekaCompetitionEskalasyon


class YekaCompetitionEskalasyonSerializer(serializers.ModelSerializer):
    class Meta:
        model = YekaCompetitionEskalasyon
        fields = '__all__'
        depth = 3