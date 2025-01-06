from django.urls import re_path
from .consumers import BeaconConsumer

websocket_urlpatterns = [
    re_path(r'ws/beacon/(?P<beacon_id>\w+)/$', BeaconConsumer.as_asgi()),
]
