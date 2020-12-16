from channels.generic.websocket import AsyncWebsocketConsumer,WebsocketConsumer
import asyncio
from channels.consumer import SyncConsumer
from asgiref.sync import async_to_sync,sync_to_async
import json
from game.models import *
class TableData(AsyncWebsocketConsumer):

    async def connect(self):
        print(self.channel_name)
        self.group_name='tableData'
        await self.channel_layer.group_add(
            self.group_name,
            self.channel_name
        )

        await self.accept()

    async def disconnect(self,close_code):
        pass

    async def receive(self,text_data):
        await self.channel_layer.group_send(
            self.group_name,
            {
                'type':'randomFunction',
                'value':text_data,
            }
        )

    async def randomFunction(self,event):
        print(event)
        value =  json.loads(event['value'])
        print(value)
        if value.get('type') == 'play_request':
            self.change_game_state(value.get('id'))
        await self.send(event['value'])
 
 
    @sync_to_async
    def change_game_state(id):
        game = Game.objects.get(id=id)
        print("############")
        print(game)
        print("############")
        game.state = 1
        game.save()

class JoinRequest(AsyncWebsocketConsumer):
    async def connect(self):
        self.group_name='joiningRequest'
        await self.channel_layer.group_add(
            self.group_name,
            self.channel_name
        )

        await self.accept()
    async def disconnect(self,close_code):
        pass

    async def receive(self,text_data):
        await self.channel_layer.group_send(
            self.group_name,
            {
                'type':'checkJoinRequest',
                'value':text_data,
            }
        )

    async def randomFunction(self,event):
        print (event['value'])
        await self.send(event['value'])
        
class Room(SyncConsumer):
    
    def websocket_connect(self):
        user = self.scope['user']
        self.room_name = self.scope['url_route']['kwargs']['room']
        async_to_sync(self.channel_layer.group_add)(self.room_name , self.channel_name)
        
        self.send({
            'type' : 'websocket.accept',
        })
        
    def websocket_receive(self, event):
        async_to_sync(self.channel_layer.group_send)(self.room_name ,{
            'type' : 'websocket.message',
            'text' : event.get('text')
        })
        
    def websocket_message(self, event):
        self.send({
            'type' : 'websocket.send',
        })
    






class ChatConsumer(WebsocketConsumer):
    def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = 'chat_%s' % self.room_name

        # Join room group
        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name,
            self.channel_name
        )

        self.accept()

    def disconnect(self, close_code):
        # Leave room group
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name,
            self.channel_name
        )

    # Receive message from WebSocket
    def receive(self, text_data):
        

        # Send message to room group
        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': text_data
            }
        )

    # Receive message from room group
    def chat_message(self, event):
        message = json.loads(event['message'])
        print(message)

        # Send message to WebSocket
        self.send(text_data=json.dumps({
            'message': message
        }))