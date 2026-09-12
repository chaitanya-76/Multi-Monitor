from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status, permissions
from django.utils import timezone
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
