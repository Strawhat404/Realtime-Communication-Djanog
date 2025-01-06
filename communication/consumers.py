from channels.generic.websocket import AsyncJsonWebsocketConsumer
import json

class BeaconConsumer(AsyncWebsocketConsumer):
    