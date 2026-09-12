from rest_framework import serializers
from .models import Device

class DeviceSerializer(serializers.ModelSerializer):
    is_online = serializers.BooleanField(read_only=True)

    class Meta:
        model = Device 
        fields = ['id', 'name', 'os_type', 'is_online', 'last_seen', 'created_at']
        read_only_fields = ['token', 'last_seen', 'created_at']