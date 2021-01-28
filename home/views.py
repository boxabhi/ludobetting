from django.shortcuts import render,redirect
from accounts.models import *
from .helpers import set_coins,fake_data,fake_running_games
from transaction.models import *
from game.models import *
from django.contrib.auth.decorators import login_required
from itertools import chain

from django.http import JsonResponse
from game.helpers import game_cron_job
from django.contrib import messages
from accounts.models import *

from .models import *
# Create your views here.




def fake_api(request):
    data = fake_data()
    return JsonResponse(data , safe=False)
    
    
def landing(request):
    if request.user.is_authenticated:
        set_coins(request)
    game_cron_job()
    images = Banners.objects.all()
    context = {'banners' : images}
    return render(request, 'home/landing.html' , context)    


def error(request):
    if request.user.is_authenticated:
        set_coins(request)
    game_cron_job()
    return render(request, 'error.html')


@login_required(login_url='/accounts/login/')
def home(request , username=None):
    local = False
    if request.user.is_authenticated:
        set_coins(request)
    data = fake_running_games()    
    if request.user.username != username:
        return redirect('/error')
    
    game_cron_job()
    pending_game_result  =  GameResult.objects.filter(user = request.user , result = 'PENDING')
    
    games = Game.objects.filter(status = 'RUNNING')
    try:
        for g in games:
            result = {}
            player_one = User.objects.get(id = g.player_one)
            player_two = User.objects.get(id = g.player_two)
            result['message'] =   f'<b>{player_one.username} vs {player_two.username}'  
            result['coins'] = g.coins
            data.append(result)    
    except Exception as e:
        print(e)
    
    
    context = {'pending_games' : pending_game_result  , 'running_games' : data , 'local' : local}  
    return render(request , 'home/index.html' , context)

@login_required(login_url='/accounts/login/')
def history(request):
    if request.user.is_authenticated:
        set_coins(request)
    
    order_coins = OrderCoins.objects.filter(user = request.user)
    sell_coins = SellCoins.objects.filter(user = request.user)
    game_results = GameResult.objects.filter(user = request.user , game__is_over=True , game__status='OVER').exclude(result='PENDING')
    penalty = Penalty.objects.filter(user = request.user)
    
    refers = ReffralTable.objects.filter(user=request.user)
    refer_bonous = ReffralBonous.objects.filter(user=request.user)
    history = History.objects.filter(user=request.user)
    results = []
    
    
    
    for h in  history:
        result = {}
        result['amount'] = h.amount
        result['message'] = h.message
        result['status'] = 'Refunded'
        result['created_at'] = str(h.created_at.strftime("%d-%m-%Y %H:%M"))
        results.append(result)
        
    
    for r in refers:
        result = {}
        result['amount'] = '0'
        result['status'] = 'Referral'
        result['message'] = (r.refer.username).upper() + ' joined via your code'
        result['created_at'] = str(r.created_at.strftime("%d-%m-%Y %H:%M"))
        results.append(result)
    
    for r in refer_bonous:
        result = {}
        result['amount'] = r.amount
        result['status'] = 'Bonous'
        result['message'] = 'You got bonous. Your refrral player won'
        result['created_at'] = str(r.created_at.strftime("%d-%m-%Y %H:%M"))
        results.append(result)
        
         
        
    for p in penalty:
        result = {}
        result['quote'] = 'Penalty'
        result['amount'] = p.amount
        result['status'] = 'Deducted'
        result['message'] = p.reason
        result['created_at'] = str(p.created_at.strftime("%d-%m-%Y %H:%M"))      
        results.append(result)
        
    
    for order_coins in order_coins:
        result = {}
        result['quote'] = 'Coins Buyed'
        
        result['amount'] = order_coins.amount
        if order_coins.status:
            result['status'] = 'Paid'
        else:
            result['status'] = 'Cancelled'
        result['message'] = 'You ordered coins'
    
        result['created_at'] = str(order_coins.created_at.strftime("%d-%m-%Y %H:%M") )       
        results.append(result)
        
    for sell_coin in sell_coins:
        result = {}
        result['quote'] = 'Sell Coins'
        result['amount'] = sell_coin.amount
        if sell_coin.is_paid:
            result['status'] = 'Paid'
        else:
            result['status'] = 'Pending'
        result['message'] = 'You Sell coins'
        
        result['created_at'] = str(sell_coin.created_at.strftime("%d-%m-%Y %H:%M"))
        results.append(result)
    count = 0
    
    for game_result in game_results:
        count+=1
        result = {}
        result['quote'] = 'Match'
    
        if game_result.result == 'CANCEL' or game_result.result == 'LOST' or game_result.result == 'QUIT':
            result['amount'] = game_result.game.coins
        elif game_result.result == 'WON':
            result['amount'] = game_result.winning_amount
        else:
            result['amount'] = game_result.game.coins
      
            
        if game_result.result == 'WON':
            result['status'] = 'Won'
        elif game_result.result == 'LOST':
            result['status'] = 'Lost'
        elif game_result.result == 'DISPUTED':
            result['status'] = 'Disputed'
        else:
            result['status'] = 'Refunded' 
        
        vs = 'Match between '
        try:
            player_one = User.objects.get(id = game_result.game.player_one)
            vs += player_one.username
            #print(player_one)
            
            
        except User.DoesNotExist:
            pass
        vs += ' V/S '
       
        try:
            player_two = User.objects.get(id = game_result.game.player_two)
            vs += player_two.username
            
            
        except User.DoesNotExist:
            pass
        result['message'] =  vs
        result['created_at'] = str(game_result.created_at.strftime("%d-%m-%Y %H:%M"))
        results.append(result)
        
    
    game_cron_job()
    history = sorted(results , key=lambda i:i ['created_at'])
    history.reverse()
    context = {'history' : history}
    return render(request , 'home/history.html' , context)

def top_winners(request):
    if request.user.is_authenticated:
        set_coins(request)
    game_cron_job()
    
    winners = TopWinners.objects.all()
    context = {'winners': winners}
    return render(request ,'home/top.html' , context)








def success(request):
    if request.user.is_authenticated:
        set_coins(request)
    return render(request , 'transaction/success.html')

def terms(request):
    return render(request ,'home/termscondition.html')


@login_required(login_url='/accounts/login/')
def refer(request):
    profile = Profile.objects.filter(user = request.user).first()
    context = {'profile': profile}
    return render(request ,'home/refer.html' , context)


def help(request):
    if request.method == 'POST':
      
        name = request.POST.get('name')
        mobile = request.POST.get('mobile')
        email = request.POST.get('email')
        problem = request.POST.get('problem')
        help = Help(name = name, mobile = mobile, email = email , problem = problem)
        help.save()
        messages.success(request, "We will get back to you!")
        return redirect('/help')
        
    return render(request ,'home/help.html')


def howtoplay(request):
    return render(request ,'home/howtoplay.html')




def quit(request):
    game_id = request.GET.get('game_id')
    game_result = GameResult.objects.filter(user = request.user , result = 'PENDING').first()
    
    
    try:
        game_obj = Game.objects.get(id = id)
        game_obj.status = 'CREATED'
        game_obj.state = 0
        
        user_profile_obj = UserProfile.objects.filter(user=game_obj.game_creater).first()
        user_profile_obj.coins += game_obj.coins

        if game_obj.player_one == str(request.user.id):
            game_obj.player_one = None
        
        if game_obj.player_two == str(request.user.id):
            game_obj.player_two = None
        game_obj.save()
        pass
    except Exception as e:
        pass
    
    if game_result:
        profile = Profile.objects.filter(user = request.user).first()
        profile.coins += game_result.game.coins 
        profile.save()
        game_result.game.coins 
        game_result.result = "QUIT"
        game_result.save()
        
        history = History(user = request.user , amount = game_result.game.coins , message = 'You quited the game')
        history.save()
        
        game = Game.objects.get(id=game_result.game.id)
    
        if str(game.player_two) == str(request.user.id):
            game.player_two = None
            game.status = 'CREATED'
            game.save()
        if str(game.player_one) == str(request.user.id):
            game.player_one = None
            game.status = 'OVER' 
            game.save()
        
        
    return redirect('/user/' + request.user.username)