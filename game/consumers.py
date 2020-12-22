from channels.generic.websocket import AsyncWebsocketConsumer,WebsocketConsumer
import asyncio
from channels.consumer import SyncConsumer
from asgiref.sync import async_to_sync,sync_to_async
import json
from game.models import *
from channels.auth import login
from django.contrib.auth.models import User
from accounts.models import *


class AllGames(WebsocketConsumer):
    http_user_and_session = True
    http_user = True
    def connect(self , **kwargs):
        self.room_name = 'all_games'
        self.group_name =  'all_games'
        async_to_sync(self.channel_layer.group_add)(
            self.group_name,
            self.channel_name
        )
        
        self.user = self.scope["user"]
        self.accept()
        data = {'type' : 'games'  , 'data' : Game.get_games(self.user)}
        self.send(text_data=json.dumps({
            'payload': data
        }))
        
    
    def disconnect(self,close_code):
        pass
    
    
    def receive(self,text_data):
        
        async_to_sync(self.channel_layer.group_send)(
            'all_game',{
                'type':'sendgames',
                'value': (text_data),
            })

    
    def sendgames(self , text_data):
        data = json.loads(text_data['value'])
        payload = {'type' : 'games'  , 'data' : data}
        self.send(text_data=json.dumps({
            'payload': data
        }))
        

    
    
    
    
    def request_game(self , text):
        print("heelo")
        

class TableData(WebsocketConsumer):
    def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['username']
        self.group_name= 'user_%s' % self.room_name
        async_to_sync(self.channel_layer.group_add)(
            self.group_name,
            self.channel_name
        )
        self.accept()
        data = Game.get_user_game(self.room_name)
        if data is None:
            data = {}
        data['type'] = 'game_created'
        self.send(text_data=json.dumps({
            'payload': data
        }))
        
        

    def disconnect(self,close_code):
        pass

    def receive(self,text_data):
        data = json.loads(text_data)
        if data.get('type') == 'request_game':
            
            
            async_to_sync(self.channel_layer.group_send)(
                'user_%s' % data.get('requested_user'),{
                    'type':'sendrequest',
                    'value': json.dumps(data),
                        }
                )
        elif data.get('type') == 'accept':
            async_to_sync(self.channel_layer.group_send)(
                'user_%s' % data.get('requested_user'),{
                    'type':'accept_request',
                    'value': json.dumps(data),
                        }
                )
        elif data.get('type') == 'declined':
            async_to_sync(self.channel_layer.group_send)(
                'user_%s' % data.get('requested_user'),{
                    'type':'decline_request',
                    'value': json.dumps(data),
                        }
                )
    
    
    def accept_request(self , text_data):
        data = json.loads(text_data['value'])
        data['type'] = 'request_accepted'
        data['message'] = 'Your request has been accepted'
        user = User.objects.filter(username=data.get('requesting_user')).first()
        game = Game.objects.filter(game_creater = user,is_over=False).first()
        user_two = User.objects.filter(username=data.get('requested_user')).first()
        game.player_two = user_two.id
        game.save()
        profile_one = Profile.objects.filter(user = user).first()
        profile_two = Profile.objects.filter(user = user_two).first()
        
        profile_one.coins = int(profile_one.coins) - int(game.coins)
        profile_one.save()
        
        profile_two.coins = int(profile_two.coins) - int(game.coins)
        profile_two.save()
        
        game_result_one = GameResult.create_game_result( game.id , user.id)
        game_result_two = GameResult.create_game_result( game.id , user_two.id )
        
        
        data['room_id'] = game.room_id
        self.send(text_data = json.dumps({
            'payload': data
        }))
        
            
    def decline_request(self, text_data):
        data = json.loads(text_data['value'])
        
        game = Game.decline_game_for_user(data.get('requesting_user') , data.get('requested_user'))
        
        if game:
            data['message'] = 'You cannot request a game more than 2 times'
        else:   
            data['message'] = 'Your request has been declined'
            
        data['type'] = 'request_declined'
        self.send(text_data = json.dumps({
            'payload': data
        }))
    

    def sendrequest(self, text_data):
        data = json.loads(text_data['value'])
        data['type'] = 'user_game'
        self.send(text_data=json.dumps({
            'payload': data
        }))
        
    
    def created_game(self , text_data):
        data = json.loads(text_data['value'])
        data['type'] = 'game_created'
        self.send(text_data = json.dumps({
            'payload': data
        }))      
    
    
    def randomFunction(self,event):
        pass
        value =  json.loads(event['value'])
        
        if value.get('type') == 'play_request':
            self.change_game_state(value.get('id'))
        self.send(event['value'])
 
 
    @sync_to_async
    def change_game_state(id):
        game = Game.objects.get(id=id)
        
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
            await self.group_name,
            {
                'type':'checkJoinRequest',
                'value':text_data,
            }
        )

    async def randomFunction(self,event):
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
        print(self.room_name)
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
        game = Game.objects.filter(room_id = self.room_name).first()
        print(game.room_code)
        if game.room_code and len(game.room_code):
            self.send(text_data=json.dumps({
                'message': {'room_code': game.room_code}
        }))
            
        

        

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
        game = Game.objects.filter(room_id = self.room_name).first()
        game.room_code =   message.get('room_code')
        game.save()
        
        # Send message to WebSocket
        self.send(text_data=json.dumps({
            'message': message
        }))