from django.shortcuts import render
from accounts.models import *
from .helpers import set_coins
from transaction.models import *
from game.models import *
from django.contrib.auth.decorators import login_required

# Create your views here.


    
    
def landing(request):
    if request.user.is_authenticated:
        set_coins(request)
    return render(request, 'home/landing.html')    


def error(request):
    if request.user.is_authenticated:
        set_coins(request)
    return render(request, 'error.html')

def home(request , username=None):
    if request.user.is_authenticated:
        set_coins(request)
        
    return render(request , 'home/index.html')

@login_required(login_url='/accounts/login/')
def history(request):
    if request.user.is_authenticated:
        set_coins(request)
    
    order_coins = OrderCoins.objects.filter(user = request.user)
    sell_coins = SellCoins.objects.filter(user = request.user)
    game_results = GameResult.objects.filter(user = request.user , game__is_over=True)
    
    results = []
    for order_coins in order_coins:
        result = {}
        result['amount'] = order_coins.amount
        if order_coins.status:
            result['status'] = 'Paid'
        else:
            result['status'] = 'Cancelled'
        result['message'] = 'You ordered coins'
        result['created_at'] = str(order_coins.created_at)        
        results.append(result)
        
    for sell_coin in sell_coins:
        result = {}
        result['amount'] = sell_coin.amount
        if sell_coin.is_paid:
            result['status'] = 'Paid'
        else:
            result['status'] = 'Pending'
        result['message'] = 'You Sell coins'
        
        result['created_at'] = str(sell_coin.created_at)
        results.append(result)
    for game_result in game_results:
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
        except User.DoesNotExist:
            pass
        vs += 'V/S'
        try:
            player_two = User.objects.get(id = game_result.game.player_two)
            vs += player_two.username
        except User.DoesNotExist:
            pass
        result['message'] = 'Match between ' +vs
        result['created_at'] = str(game_result.created_at)
        results.append(result)
        

    history = sorted(results , key=lambda i:i ['created_at'])
    
    context = {'history' : history}
    print(context)
    return render(request , 'home/history.html' , context)

def top_winners(request):
    if request.user.is_authenticated:
        set_coins(request)
    return render(request ,'home/top.html')