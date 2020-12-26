from django.shortcuts import render,redirect
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import *
from accounts.models import *
import pusher
import uuid
import json
from home.helpers import *
from django.contrib import messages
import time
# Create your views here.


def game_playing(request):
    return render(request, 'game/game_playing.html')

def waiting_room(request , room_id):
    if request.user.is_authenticated:
        set_coins(request)
        
    game = Game.objects.filter(room_id=room_id).first()
    user = request.user
    if game is None:
        return redirect('/error')
     

    
    if request.method == 'POST':
        result = request.POST.get('result')
        images = request.FILES.getlist('upload_file')
        reason_of_cancel = request.POST.get('reason_of_cancel')
        
        
        
        if game.room_code is None :
            messages.success(request, 'Something went wrong You must enter room code 😒')
            return redirect('/game/room/' + str(game.room_id) )
            
        game_result = GameResult.objects.filter(game=game , user=user , result="PENDING").first()
        if game_result is None :
            game_result,_ = GameResult.objects.get_or_create(game = game , user = user , result='PENDING')
        game_result.result = result
        
        if result == 'WON' and not len(images):
            messages.success(request, 'If you have won you must upload game winning images 😒')
            return redirect('/game/room/' + str(game.room_id) )
        
        if result == 'CANCEL' and not len(reason_of_cancel):
            messages.success(request, 'If your game got CANCEL enter reason 😒')
            return redirect('/game/room/' + str(game.room_id) )
            
        
        if reason_of_cancel:
            game_result.reason_of_cancel = reason_of_cancel
        game_result.save()
        
        for image in images:
            image_obj = Image(user = user,game =game,game_result =game_result,uploaded_image=image)
            image_obj.save()
        
        game.is_over = True
        if game.player_one is not None and request.user.id == game.player_one:
            game.result_by_player_one = request.user
            game.state +=1 
            game.save()
        if game.player_one is not None and request.user.id  == game.player_two:
            game.result_by_player_two = request.user
        game.state +=1 
        game.save()
        
        messages.success(request, 'Result Updated')
        return redirect('/user/' + request.user.username)
    
    
    
    
    
    if game.player_one is None or game.player_two is None:
        messages.success(request, "Second player did'nt joins")
        return redirect('/user/' + request.user.username)
    
    user_one = User.objects.get(id = game.player_one)
    user_two = User.objects.get(id = game.player_two)
    
    
    context = {'room_id': room_id , 'game' : game , 'user_one' : user_one , 'user_two' : user_two}
    
    
    return render(request, 'game/waiting_room.html' , context)



def delete_game(request , id):
    user = request.user
    try:
        game = Game.objects.get(id=id)
        if game.game_creater.id != user.id:
            return redirect('/user/'+user.username +'/')
        else:
            game.delete()
            return redirect('/user/'+user.username +'/')
    except Game.DoesNotExist:
        return redirect('/user/'+user.username +'/')





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
        game = Game.objects.filter(game_creater = user , is_over=False).first()
        if game is None:
            game, _ = Game.objects.get_or_create(game_creater = user , is_over=False)
        game.coins = coins
        game.player_one = user.id
        game.room_id = room_id
        game.save()
        
        payload = { 'coins' : game.coins, 'room_id' : str(room_id)}
        return JsonResponse({'message': 'Game Created' , 'status':True , 'payload' : payload})
        
    else:
        return JsonResponse({'error': 'You are not authenticated!'} , safe=False)
    