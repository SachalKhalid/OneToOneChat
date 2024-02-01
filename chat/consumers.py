import json
from .models import Message, Room, User
from asgiref.sync import sync_to_async
from channels.generic.websocket import WebsocketConsumer
from channels.generic.websocket import AsyncWebsocketConsumer

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = self.scope["url_route"]["kwargs"]["room_name"]
        self.room_group_name = f"chat_{self.room_name}"

        # Join room group
        await self.channel_layer.group_add(self.room_group_name, self.channel_name)

        await self.accept()

    async def disconnect(self, close_code):
        # Leave room group
        await self.channel_layer.group_discard(self.room_group_name, self.channel_name)

    # Receive message from WebSocket
    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json["message"]
        username = text_data_json["username"]
        room = text_data_json["room"]
        timestamp = text_data_json["timestamp"]
        print(type(message), type(username), type(room), timestamp)
        await self.save_message(username, room, message)

        # Send message to room group
        await self.channel_layer.group_send(
            self.room_group_name, {
                "type": "chat.message", 
                "message": message,
                'username': username
                
                }
        )

    # Receive message from room group
    async def chat_message(self, event):
        message = event["message"]
        username = event['username']
        # Send message to WebSocket
        await self.send(text_data=json.dumps({
            "message": message,
            "username" : username
            }))
        
    @sync_to_async
    def save_message(self, username, room_name, message):
        try:
            room = Room.objects.get(name=room_name)
            user = User.objects.get(username=username)
            Message.objects.create(user=user, room=room, content=message)
        except Room.DoesNotExist:
            print(f"Room with name {room_name} does not exist.")
        except User.DoesNotExist:
            print(f"User with username {username} does not exist.")
        except Exception as e:
            print(f"An error occurred: {str(e)}")
