"""assuming we have already models like
-BeaconDevices
-ProximityEvent
-NotificationEvent"""

from rest_framework import serializers
from .models import BeaconDevice,ProximityEvent,NotificationEvent

class BeaconDeviceSerializer(serializers.ModelSerializer):
    class Meta:
        model = BeaconDevice
        fields = '__all__'
class ProximityEventSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProximityEvent
        fields = '__all__'
        
class NotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notification
        fileds = '__all__'