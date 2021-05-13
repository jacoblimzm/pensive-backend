# allows us to create an  app that's asynchronous
from channels.generic.websocket import AsyncWebsocketConsumer
import json
# from chat_room.models import 

class ChatRoomConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        # captured groups from routing.py in the urls will be attached to scope.
        self.room_name = self.scope["url_route"]["kwargs"]["room_name"]
        
        # using a group allows us to broadcast messages to users inside the group
        self.room_group_name = f"chat_{self.room_name}"
        
        # any consumer based on channel's SyncConsumer or AsyncConsumer will auto provide a self.channel_layer AND self.channel_name 
        # which contains a pointer to the channel layer instance and channel name that will reach the consumer
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )
        await self.accept()
        
    # the "type" of the event in group_send() below determines the named method of the consumer, with "." replaced by "_"
    async def chat_message(self, event):
        
        await self.send(text_data=json.dumps({
            **event, # this is a more flexible way of sending the message using python unpacking -> JS destructuring equivalent
        }))        
        # {
        #     "name": event["name"],
        #     "message": event["message"]
        # }
        
    async def receive(self, text_data):
        # receives a json message from the front end and deserialises it into a Python object
        # to be stored in the database?
        # messages handled through here
        text_data_json = json.loads(text_data)
        
        # name = text_data_json["name"]
        # message = text_data_json["message"]
        
        # an event coming in over the channel layer with "type" chat.message. handled by chat_message() below
        # again uses the chat_message() function to send the message as a JSON object
        await self.channel_layer.group_send(
            self.room_group_name,
            {
               "type": "chat.message",
               **text_data_json,
            }
        )    
            
    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name,
        )
        