from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status, permissions
from rest_framework.generics import ListAPIView
from rest_framework.exceptions import PermissionDenied
from django.utils import timezone
from devices.models import Device
from .models import Telementry
from .serializers import TelementrySerializer
from devices.authentication import DeviceTokenAuthentication

class TelementryCreateView(APIView):
    authentication_classes = [DeviceTokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        device = request.auth 
        serializer = TelementrySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(device=device)
            device.last_seen = timezone.now()
            device.save(update_fields=['last_seen'])
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class HeartbeatView(APIView):
    authentication_classes = [DeviceTokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request): 
        device = request.auth
        device.last_seen = timezone.now()
        device.save(update_fields=['last_seen'])
        return Response({'status':'ok', 'last_seen': device.last_seen})

class DeviceTelementryListView(ListAPIView):
    serializer_class = TelementrySerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        device_id = self.kwargs['device_id']
        device = Device.objects.filter(id=device_id, owner=self.request.user).first()
        if not device:
            raise PermissionDenied("Deivce not found or not yours")
        return Telementry.objects.filter(device=device)[:20]