from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import *
from accounts.models import *
import pusher
import uuid
import json
# Create your views here.


pusher_client = pusher.Pusher(
  app_id='1123072',
  key='c8c9c5c7311851c8d82d',
  secret='5de35561e0a1814c29c2',
  cluster='ap2',
  ssl=True
)


def game_playing(request):
    return render(request, 'game/game_playing.html')

@csrf_exempt
def games(request):
    pusher_client.trigger('my-channel', 'my-event', {'message': 'hello world'})
    message = {'message': 'hello world'}
    return JsonResponse(message, safe=False)

@csrf_exempt
def create_game(request):
    user = request.user
    data = json.loads(request.body)
    if request.user.is_authenticated and request.method == 'POST':
        coins = data.get('coins')
        profile = Profile.objects.filter(user = user).first()
        
        if coins is None:
            return JsonResponse({'message': 'Coins is required','status':False })
        
        if int(profile.coins) < int(coins):
            return JsonResponse({'message' : "You don't have sufficient coins! 😧" ,'status':False})
        
        room_id = uuid.uuid4()
        game, _ = Game.objects.get_or_create(game_creater = user , is_over=False)
        game.coins = coins
        game.player_one = user.id
        game.room_id = room_id
        game.save()
        
        payload = { 'coins' : game.coins, 'room_id' : str(room_id)}
        return JsonResponse({'message': 'Game Created' , 'status':True , 'payload' : payload})
        
    else:
        return JsonResponse({'error': 'You are not authenticated!'} , safe=False)
    