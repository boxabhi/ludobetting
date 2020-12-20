from django.shortcuts import render,redirect
from accounts.models import  *
from transaction.models import *
from game.models import *
from django.core.paginator import Paginator
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib import messages

# Create your views here.






def index(request):
    return render(request, 'admin/admin-home.html')

def userlist(request):
    profiles = Profile.objects.all()
    context = {'profiles' : profiles}
    return render(request, 'admin/userlists.html' , context)

def viewuser(request , profile_id):
    context = {}
    try:
        profile = Profile.objects.get(id = profile_id)
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
        for game_result in game_results:
            count+=1
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
            result['message'] = 'Match between ' +vs
            result['created_at'] = str(game_result.created_at)[0:11]
            results.append(result)
            
        print(count)
        history = sorted(results , key=lambda i:i ['created_at'])
        context = {'profile': profile ,'history' : history}
    except Profile.DoesNotExist:
        return redirect('/error')
    return render(request, 'admin/viewuser.html' , context)


def disputesgame(request):
    disputeds = DisputedGame.objects.all()
    context = {'disputeds':disputeds}
    
    return render(request, 'admin/disputeslist.html'  , context)


def viewdisputes(request):
    return render(request, 'admin/viewdisputes.html')




def total_purchase(request):
    objects  = OrderCoins.objects.all()
    paginator  = Paginator(objects, 20)
    page  = request.GET.get('page' , 1)
    try:
        page_obj = paginator.page(page)
    except PageNotAnInteger:
        page_obj = paginator.page(1)
    except EmptyPage:
        page_obj= paginator.page(paginator.num_pages)
    context = {'order_coins'  : objects , 'page_obj': page_obj}
    print(page_obj)
    return render(request, 'admin/total_purchase.html' , context)




def sellcoinsrequest(request):
    objects = SellCoins.objects.all()
    
    paginator  = Paginator(objects, 2)
    page  = request.GET.get('page' , 1)
    try:
        page_obj = paginator.page(page)
    except PageNotAnInteger:
        page_obj = paginator.page(1)
    except EmptyPage:
        page_obj= paginator.page(paginator.num_pages)
        
    context = {'page_obj': page_obj}
    for p in page_obj:
        print(p)
    return render(request, 'admin/sellcoinsrequests.html' , context)

def paycoins(request):
    return render(request, 'admin/paycoins.html')

def penalty(request):
    if request.method == 'POST':
        amount = request.POST.get('amount')
        whatsapp = request.POST.get('whatsapp')
        username = request.POST.get('username')
        reason = request.POST.get('reason')
        
        user = None
        
        if whatsapp:
            user = Profile.objects.filter(whatsapp = whatsapp).first()
            if user is None:
                messages.success(request, 'User not found 🧐')
                return redirect('/paneladmin/penalty/')
            else:
                penalty = Penalty(user = user.user , amount = amount ,reason=reason)
                penalty.save()
        elif username:
            user = User.objects.filter(username=username).first()
            if user is None:
                messages.success(request, 'User not found 🧐')
                return redirect('/paneladmin/penalty/')
            else:
                penalty = Penalty(user = user , amount = amount ,reason=reason)
                penalty.save()
        messages.success(request, 'Penalty added successfully 🧐')
        return redirect('/paneladmin/penalty/')
    return render(request, 'admin/penalty.html')


def show_penalty(request):
    objects = Penalty.objects.all()
    paginator  = Paginator(objects, 2)
    page  = request.GET.get('page' , 1)
    try:
        page_obj = paginator.page(page)
    except PageNotAnInteger:
        page_obj = paginator.page(1)
    except EmptyPage:
        page_obj= paginator.page(paginator.num_pages)
        
    context = {'page_obj': page_obj}
    return render(request, 'admin/show_penalty.html' , context)
    
    



