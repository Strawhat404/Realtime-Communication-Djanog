from channels.generic.websocket import AsyncWebsocketConsumer
import json

class ChatConsumer(AsynchWebsocketConsumer):
    async def connect(self):
        self.room_group_name = "chat_general"
        
        #join room group
       await self.channel_layer.group_add(
           self.room_group_name,
           self.channel_name
       ) 
       await self.accept()
       
    async def disconnect(self,close_code):
        #leave a room
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )
        
    async def recieve (self,text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']
        
        #send message to the room
        
        
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type':'chat_message',
                'message': message
            }
        )
    async def chat_message(self, event):
        message = event['message']
    
    #sending a message to a websocket
        await self.send(text_data=json.dumps({
            'message': message
        }))
        
        