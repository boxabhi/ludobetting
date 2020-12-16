from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
import channels.layers
from django.dispatch import receiver
from asgiref.sync import async_to_sync
import json
# Create your models here.


RESULT = (
    ('WON', 'WON'),
    ('LOST' , 'LOST'),
    ('CANCEL' , 'CANCEL')
)

class Game(models.Model):
    game_creater = models.ForeignKey(User, on_delete=models.CASCADE)
    coins = models.IntegerField(default=0)
    room_id = models.CharField(max_length=100)
    player_one = models.CharField(max_length=10 ,blank=True , null=True)
    player_two = models.CharField(max_length=10 , blank=True , null=True)
    requested_players = models.CharField(max_length=100 , blank=True , null=True)
    is_over = models.BooleanField(default=False)
    state = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    


    
class GameResult(models.Model):
    game = models.ForeignKey(Game, on_delete=models.CASCADE , null=True , blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE , null=True , blank=True)
    result = models.CharField(max_length=25 , choices = RESULT)
    reason_of_cancel = models.TextField(blank=True , null=True)


class Image(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE , null=True , blank=True)
    game_result = models.ForeignKey(GameResult , on_delete=models.CASCADE , null=True , blank=True)
    uploaded_image = models.ImageField(upload_to = 'static/images')

    

    
    
    
    
@receiver(post_save, sender=Game)
def game_handler(sender , instance,created,**kwargs): 
    print(instance)
    print(created)
    if created or not created:
        channel_layer = channels.layers.get_channel_layer()
        data = {}
        data['id'] = instance.id
        data['game_creater'] = instance.game_creater.username
        data['coins'] = instance.coins
        data['room_id'] = str(instance.room_id)
        data['player_one'] = instance.player_one
        
        print(data)
        async_to_sync(channel_layer.group_send)(
            'tableData',
            {
            'type': 'randomFunction',
            'value': json.dumps(data)
            }
        )
