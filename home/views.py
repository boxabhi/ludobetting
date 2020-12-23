from django.shortcuts import render,redirect
from accounts.models import *
from .helpers import set_coins,fake_data,fake_running_games
from transaction.models import *
from game.models import *
from django.contrib.auth.decorators import login_required
from itertools import chain

from django.http import JsonResponse
# Create your views here.




def fake_api(request):
    data = fake_data()
    return JsonResponse(data , safe=False)
    
    
def landing(request):
    if request.user.is_authenticated:
        set_coins(request)
    return render(request, 'home/landing.html')    


def error(request):
    if request.user.is_authenticated:
        set_coins(request)
    return render(request, 'error.html')


@login_required(login_url='/accounts/login/')
def home(request , username=None):
    if request.user.is_authenticated:
        set_coins(request)
    data = fake_running_games()    
    if request.user.username != username:
        return redirect('/error')
    
    
    pending_game_result  =  GameResult.objects.filter(user = request.user , result = 'PENDING') 
    context = {'pending_games' : pending_game_result  , 'running_games' : data}  
    return render(request , 'home/index.html' , context)

@login_required(login_url='/accounts/login/')
def history(request):
    if request.user.is_authenticated:
        set_coins(request)
    
    order_coins = OrderCoins.objects.filter(user = request.user)
    sell_coins = SellCoins.objects.filter(user = request.user)
    game_results = GameResult.objects.filter(user = request.user , game__is_over=True , game__status='OVER').exclude(result='PENDING')
    results = []
    for order_coins in order_coins:
        result = {}
        result['amount'] = order_coins.amount
        if order_coins.status:
            result['status'] = 'Paid'
        else:
            result['status'] = 'Cancelled'
        result['message'] = 'You ordered coins'
        result['created_at'] = str(order_coins.created_at)[0:10]       
        results.append(result)
        
    for sell_coin in sell_coins:
        result = {}
        result['amount'] = sell_coin.amount
        if sell_coin.is_paid:
            result['status'] = 'Paid'
        else:
            result['status'] = 'Pending'
        result['message'] = 'You Sell coins'
        
        result['created_at'] = str(sell_coin.created_at)[0:11]
        results.append(result)
    count = 0
    print(game_results)
    for game_result in game_results:
        count+=1
        result = {}
        result['amount'] = game_result.game.coins
        if game_result.result == 'WON':
            result['status'] = 'Won'
        elif game_result.result == 'LOST':
            result['status'] = 'Lost'
        else:
            result['status'] = 'Cancel' 
        
        vs = 'Match between '
        try:
            player_one = User.objects.get(id = game_result.game.player_one)
            vs += player_one.username
            #print(player_one)
            
            
        except User.DoesNotExist:
            pass
        vs += ' V/S '
        print(game_result.game.player_two)
        try:
            player_two = User.objects.get(id = game_result.game.player_two)
            vs += player_two.username
            print(player_two)
            
        except User.DoesNotExist:
            pass
        result['message'] =  vs
        result['created_at'] = str(game_result.created_at)[0:11]
        results.append(result)
        
    print(count)
    history = sorted(results , key=lambda i:i ['created_at'])
    
    context = {'history' : history}
    
    return render(request , 'home/history.html' , context)

def top_winners(request):
    if request.user.is_authenticated:
        set_coins(request)
    return render(request ,'home/top.html')








def success(request):
    if request.user.is_authenticated:
        set_coins(request)
    return render(request , 'transaction/success.html')

def terms(request):
    return render(request ,'home/termscondition.html')


def help(request):
    return render(request ,'home/help.html')


def howtoplay(request):
    return render(request ,'home/howtoplay.html')

