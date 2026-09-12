from rest_framework import serializers
from .models import Telementry

class TelementrySerializer(serializers.ModelSerializer):
    class Meta:
        model = Telementry
        fields = ['id', 'timestamp', 'cpu_percent', 'memory_percent', 'disk_percent']
        read_only_fields = ['id', 'timestamp']