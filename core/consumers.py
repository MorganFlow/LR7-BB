import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from rest_framework_simplejwt.tokens import UntypedToken
from django.contrib.auth.models import User

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        token = self.scope['query_string'].decode().split('token=')[-1]
        try:
            validated_token = UntypedToken(token)
            user_id = validated_token['user_id']
            self.user = await database_sync_to_async(User.objects.get)(id=user_id)
            await self.channel_layer.group_add("global_chat", self.channel_name)
            await self.accept()
        except:
            await self.close()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard("global_chat", self.channel_name)

    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']
        await self.channel_layer.group_send(
            "global_chat",
            {
                'type': 'chat_message',
                'message': message,
                'username': self.user.username
            }
        )

    async def chat_message(self, event):
        await self.send(text_data=json.dumps({
            'message': event['message'],
            'username': event['username']
        }))