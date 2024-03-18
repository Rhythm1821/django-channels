import json
from channels.generic.websocket import WebsocketConsumer
from asgiref.sync import async_to_sync

class ChatConsumer(WebsocketConsumer):
    def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = f"chat_{self.room_name}"

        # Join group name
        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name,self.channel_name
        )

        self.accept()
    
    def disconnect(self, code):
        # Leave room group 
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name,self.channel_name
        )
    
    # Recieve message from websocket
    def receive(self, text_data=None):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']

        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name,{"type":"chat.message","message":message}
        )
    
    # Recieve message from room group
    def chat_message(self,event):
        message = event['message']

        # Send message to websocket
        self.send(text_data=json.dumps({"message":message}))