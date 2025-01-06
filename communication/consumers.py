from channels.generic.websocket import AsyncJsonWebsocketConsumer
import json

class BeaconConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name  = self.scope['url_route']['kwargs']['beacon_id']
        self.room_group_name = f"beacon_{self.room_name}"
        
        #join the group section
        
        await self.channel_layer.group_add(self.room_group_name, self.channel_name)
        await.self.accept()
        
    async def disconnect(self,close_code):
        #a section to leave the group
        
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )
    async def recieve(self,text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']
        
        
        #send the message to group
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type':'beacon_message',
                'message':message
            }
        )
    async def beacon_message(self,event):
        message = event['message']
        
        
        
        #sending message to Websocket
        await self.send(text_data=json.dumps({
            'message':message
        }))