from django.urls import re_path
from rideapp.consumers import RideTrackingConsumer

websocket_urlpatterns = [
    re_path(r'ws/ride_tracking/$', RideTrackingConsumer.as_asgi()),
]
