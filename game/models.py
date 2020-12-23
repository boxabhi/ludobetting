from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save, post_delete
import channels.layers
from django.dispatch import receiver
from asgiref.sync import async_to_sync
import json
from django.core import serializers
from channels.layers import get_channel_layer
from accounts.models import *
# Create your models here.


RESULT = (
    ('PENDING', 'PENDING'),
    ('WON', 'WON'),
    ('LOST' , 'LOST'),
    ('CANCEL' , 'CANCEL')
)

STATUS = (
    ('CREATED' , 'CREATED'),
    ('RUNNING' , 'RUNNING'),
    ('WAITING' , 'WAITING'),
    ('OVER' , 'OVER'),
)

class Game(models.Model):
    game_creater = models.ForeignKey(User, on_delete=models.CASCADE)
    coins = models.IntegerField(default=0)
    room_id = models.CharField(max_length=100)
    player_one = models.CharField(max_length=10 ,blank=True , null=True)
    player_two = models.CharField(max_length=10 , blank=True , null=True)
    requested_players = models.CharField(max_length=500 , default=',')
    is_over = models.BooleanField(default=False)
    state = models.IntegerField(default=0)
    status = models.CharField(max_length=100 , choices=STATUS , default='CREATED')
    created_at = models.DateTimeField(auto_now_add=True)
    result_by_player_one = models.ForeignKey(User, related_name='result_by_player_one', on_delete=models.CASCADE , blank=True , null=True)
    result_by_player_two = models.ForeignKey(User, related_name='result_by_player_two' ,on_delete=models.CASCADE , blank=True , null=True)
    room_code = models.CharField(max_length=100 , blank=True , null=True)
    
    def __str__(self):
        return 'Game by - ' + self.game_creater.username + ' (' + str(self.room_id) + ')'
    
    @staticmethod
    def get_running_games():
        games = Game.objects.filter(status = 'RUNNING')
        payload = []
        for game in games:
            result = {}
            result['id'] = game.id
            user_one = User.objects.get(id = game.player_one)
            user_two = User.objects.get(id = game.player_two)
            result['message'] = user_one.username + ' vs ' + user_two.username
            payload.append(result)
        return payload
       
        
    
    @staticmethod
    def get_games(user_id):
        games = Game.objects.filter(is_over = False).exclude(game_creater = user_id)
        payload = []
        for game in games:
            result = {}
            if not game.is_over:
                result['id'] = game.id
                result['game_creater'] = game.game_creater.username
                result['coins']  = game.coins
                result['room_id'] = game.room_id
                result['state'] = game.state
                payload.append(result)
            
        return payload

    @staticmethod
    def get_user_game(username):
        
        user = User.objects.filter(username=username).first()
        game = Game.objects.filter(game_creater =user , is_over=False).first()
        if game is None:
            return None
        payload = {}
        payload['id'] = game.id
        payload['game_creater'] = game.game_creater.username
        payload['coins']  = game.coins
        payload['room_id'] = game.room_id
        payload['state'] = game.state
        return payload
            
    @staticmethod
    def decline_game_for_user(requesting_user ,requested_user ):
        user = User.objects.filter(username=requesting_user).first()
        game = Game.objects.filter(game_creater = user,is_over=False).first()
        
        check_user_exits = game.requested_players.split(',')
    
        if check_user_exits.count(requested_user) > 2:
            return True
        game.requested_players += ',' + requested_user
        game.save()
        return False
        
        
    

    
    
class GameResult(models.Model):
    game = models.ForeignKey(Game, on_delete=models.CASCADE , null=True , blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE , null=True , blank=True)
    result = models.CharField(max_length=25 , choices = RESULT ,  default='PENDING')
    reason_of_cancel = models.TextField(blank=True , null=True)
    created_at = models.DateTimeField(auto_now=True)

    
    @staticmethod
    def create_game_result(game_id , user_id):
       
        game = Game.objects.get(id = game_id)
        user = User.objects.get(id = user_id)   
        game_result = GameResult(game = game , user = user)
        game_result.save()
    
    def __str__(self):
        return 'Game result by  - ' + self.user.username + ' (' + self.game.room_id + ')'
 
# @receiver(post_save, sender=GameResult)
# def game_result_handler(sender , instance,created,**kwargs):
#     game = Game.objects.get(id = instance.game.id)    
#     check_game_result = GameResult.objects.filter(game = game)
#     game.is_over = True
#     game.save()
#     if len(check_game_result) == 2:
#         print(check_game_result)
#         game.status = 'OVER'
#         game.save()
#         game_result_obj_one =    check_game_result[0]
#         game_result_obj_two =    check_game_result[1]
#         print(game_result_obj_one.result)
#         print(game_result_obj_two.result)
        
#         if game_result_obj_one.result == 'WON' and game_result_obj_one.result == 'LOST':
#             winner = Profile.objects.filter(user = game_result_obj_one.user).first()
#             winner.coins +=  (.95 * game.coins)
#             game_result_obj_one.result  = 'WON'
#             game_result_obj_one.save()
#             winner.save()
#             game.status = 'OVER'
#             game.save()
#         elif game_result_obj_one.result == 'LOST' and game_result_obj_one.result == 'WON':
#             winner = Profile.objects.filter(user = game_result_obj_two.user).first()
#             winner.coins +=  (.95 * game.coins)
#             game_result_obj_two.result  = 'WON'
#             game_result_obj_two.save()
#             winner.save()
#         elif game_result_obj_one.result == 'CANCEL' and game_result_obj_one.result == 'CANCEL':
#             user_obj_one = Profile.objects.filter(user = game_result_obj_one.user).first()
#             user_obj_two = Profile.objects.filter(user = game_result_obj_two.user).first()
            
#             user_obj_one.coins += game.coins
#             user_obj_two.coins += game.coins
            
#             user_obj_one.save()
#             user_obj_two.save()
#             game.status = 'OVER'
#             game.save()
            
#             game_result_obj_two.result  = 'CANCEL'
#             game_result_obj_one.result  = 'CANCEL'
#             game_result_obj_two.save()
#             game_result_obj_one.save()

#         elif game_result_obj_one.result == 'WON' and game_result_obj_two.result == 'WON':
#             disputed = DisputedGame(game = game)
#             disputed.save()
           
        
             
    

class Image(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE , null=True , blank=True)
    game = models.ForeignKey(Game , on_delete=models.CASCADE , blank=True , null=True)
    game_result = models.ForeignKey(GameResult , on_delete=models.CASCADE , null=True , blank=True)
    uploaded_image = models.ImageField(upload_to = 'static/images')
    
    def __str__(self):
        return self.user.username + ' ' + self.game_result.game.room_id


    



class DisputedGame(models.Model):
    game = models.ForeignKey(Game  , on_delete=models.CASCADE)
    winner = models.ForeignKey(User , on_delete=models.CASCADE , blank=True , null=True)
    is_reviewed = models.BooleanField(default=False)
    
    def __str__(self):
        return  str(self.is_reviewed)


@receiver(post_save, sender=DisputedGame)
def disputed_handler(sender , instance,created,**kwargs):
    
    if instance.winner:
        game = Game.objects.get(id = instance.game.id)
        game.status = 'OVER'
        profile = Profile.objects.get(id = instance.winner.id)
        profile.coins += game.coins
        profile.save()



@receiver(post_delete, sender=Game)
def game_delete(sender , instance,**kwargs):
    channel_layer = channels.layers.get_channel_layer()
    games = Game.objects.filter(is_over = False)
    payload = []
    for game in games:
        result = {}
        if not game.is_over:
            result['id'] = game.id
            result['game_creater'] = game.game_creater.username
            result['coins']  = game.coins
            result['room_id'] = game.room_id
            result['state'] = game.state
            payload.append(result)
    async_to_sync(channel_layer.group_send)(
        'all_games',{
        'type': 'sendgames',
        'value': json.dumps({'data' : payload , 'type' : 'games'})
        })
    
@receiver(post_save, sender=Game)
def game_handler(sender , instance,created,**kwargs): 
    print(instance)
    channel_layer = channels.layers.get_channel_layer()
    if created is False:
        games = Game.objects.filter(is_over = False)
        payload = []
        for game in games:
            result = {}
            if not game.is_over:
                result['id'] = game.id
                result['game_creater'] = game.game_creater.username
                result['coins']  = game.coins
                result['room_id'] = game.room_id
                result['state'] = game.state
                payload.append(result)
  
        async_to_sync(channel_layer.group_send)(
            'all_games',{
            'type': 'sendgames',
            'value': json.dumps({'data' : payload , 'type' : 'games'})
            }
        )
    
    if created or not created:
        data = {}
        data['id'] = instance.id
        data['game_creater'] = instance.game_creater.username
        data['coins'] = instance.coins
        data['room_id'] = str(instance.room_id)
        data['player_one'] = instance.player_one
        
        async_to_sync(channel_layer.group_send)(
            'user_%s' % instance.game_creater.username,{
                'type': 'created_game',
                'value': json.dumps(data)
            }
        )
        
        games = Game.objects.filter(is_over = False)
        payload = []
        for game in games:
            result = {}
            if not game.is_over:
                result['id'] = game.id
                result['game_creater'] = game.game_creater.username
                result['coins']  = game.coins
                result['room_id'] = game.room_id
                result['state'] = game.state
                payload.append(result)
        async_to_sync(channel_layer.group_send)(
            'all_games',{
            'type': 'sendgames',
            'value': json.dumps({'data' : payload , 'type' : 'games'})
            }
        )
