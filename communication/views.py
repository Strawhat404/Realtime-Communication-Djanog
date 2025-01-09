from rest_framework import viewset
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import BeaconDevice, ProximityEvent, Notification
from .serializers import BeaconDeviceSerializer, ProximityEventSerializer, NotificationSerializer


class BeaconDeviceViewSet(viewsets.ModelViewSet):
    queryset = BeaconDevice.objects.all()
    serializer_class = BeaconDeviceSerializer
    
    @action(detail=True,methods = ['GET'])
    def events(self,request,pk=None):
        beacon = self.get_object()
        events = ProximityEvent.objects.filter(beacom = beacon)
        serializer = ProximityEventSerializer(events,many=True)
        return Response (serializer.data)
        