from django.urls import path
from .views import TelementryCreateView, HeartbeatView

urlpatterns = [
    path('telementry/', TelementryCreateView.as_view(), name='telementry-create'),
    path('heartbeat/', HeartbeatView.as_view(), name='heartbeat')
]