from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class Game(models.Model):
    game_creater = models.ForeignKey(User, on_delete=models.CASCADE)
    coins = models.IntegerField(default=0)
    room_id = models.CharField(max_length=100)
    player_one = models.CharField(max_length=10 ,blank=True , null=True)
    player_two = models.CharField(max_length=10 , blank=True , null=True)
    requested_players = models.CharField(max_length=100 , blank=True , null=True)
    is_over = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    
    