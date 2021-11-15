from rest_framework import serializers

from ekabis.models import NotificationUser


class NotificationUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = NotificationUser
        fields = '__all__'
        depth = 3