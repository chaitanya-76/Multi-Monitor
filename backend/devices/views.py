from django.shortcuts import render
from rest_framework import viewsets, permissions
from .models import Device
from .serializers import DeviceSerializer

# Create your views here.

class DeviceViewSet(viewsets.ModelViewSet):
    serializer_class = DeviceSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Device.objects.filter(owner=self.request.user)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

