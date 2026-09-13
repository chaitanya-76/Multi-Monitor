from django.urls import path
from .views import TelementryCreateView, HeartbeatView, DeviceTelementryListView

urlpatterns = [
    path('telementry/', TelementryCreateView.as_view(), name='telementry-create'),
    path('heartbeat/', HeartbeatView.as_view(), name='heartbeat'),
    path('devices/<int:device_id>/telementry/', DeviceTelementryListView.as_view(), name='device-telementry'),
]