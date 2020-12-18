from django.shortcuts import render
from accounts.models import *
from .helpers import set_coins
from transaction.models import *
from django.contrib.auth.decorators import login_required

# Create your views here.


    
    

def home(request):
    if request.user.is_authenticated:
        set_coins(request)
        
    return render(request , 'home/index.html')

@login_required(login_url='/accounts/login/')
def history(request):
    if request.user.is_authenticated:
        set_coins(request)
    
    order_coins = OrderCoins.objects.filter(user = request.user)
    sell_coins = SellCoins.objects.filter(user = request.user)
    
    
    
    return render(request , 'home/history.html')

def top_winners(request):
    return render(request ,'home/top.html')

def terms(request):
    return render(request ,'home/termscondition.html')


def help(request):
    return render(request ,'home/help.html')


def howtoplay(request):
    return render(request ,'home/howtoplay.html')