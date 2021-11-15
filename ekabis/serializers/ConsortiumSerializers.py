from rest_framework import serializers

from ekabis.models.ConsortiumCompany import ConsortiumCompany
from ekabis.models.District import District


class ConsortiumSerializer(serializers.ModelSerializer):
    class Meta:
        model = ConsortiumCompany
        fields = '__all__'
        depth = 3