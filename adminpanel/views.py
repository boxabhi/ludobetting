from django.shortcuts import render,redirect
from accounts.models import  *
from transaction.models import *
from game.models import *
from django.core.paginator import Paginator
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib import messages

# Create your views here.






def index(request):
    return render(request, 'admin_panel/admin-home.html')

def userlist(request):
    profiles = Profile.objects.all()
    context = {'profiles' : profiles}
    return render(request, 'admin_panel/userlists.html' , context)

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
    return render(request, 'admin_panel/viewuser.html' , context)


def disputesgame(request):
    objects = DisputedGame.objects.all()
    paginator  = Paginator(objects, 20)
    page  = request.GET.get('page' , 1)
    try:
        page_obj = paginator.page(page)
    except PageNotAnInteger:
        page_obj = paginator.page(1)
    except EmptyPage:
        page_obj= paginator.page(paginator.num_pages)
    context = {'page_obj': page_obj}

    return render(request, 'admin_panel/disputeslist.html'  , context)


def viewdisputes(request , disputed_id):
    context = {}
    try:
        diputed_game = DisputedGame.objects.get(id = disputed_id)
        game_result = GameResult.objects.filter(game = diputed_game.game).first()
        images = Image.objects.filter(game_result = game_result)
        context = {'diputed_game' : diputed_game , 'game_result' : game_result , 'images' : images}
    except DisputedGame.DoesNotExist:
        return redirect('/error')
    return render(request, 'admin_panel/viewdisputes.html' , context)




def total_purchase(request):
    objects  = OrderCoins.objects.all()
    paginator  = Paginator(objects, 2)
    page  = request.GET.get('page' , 1)
    try:
        page_obj = paginator.page(page)
    except PageNotAnInteger:
        page_obj = paginator.page(1)
    except EmptyPage:
        page_obj= paginator.page(paginator.num_pages)
    context = {'order_coins'  : objects , 'page_obj': page_obj}
    print(page_obj)
    return render(request, 'admin_panel/total_purchase.html' , context)




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
    return render(request, 'admin_panel/sellcoinsrequests.html' , context)

def paycoins(request):
    return render(request, 'admin_panel/paycoins.html')

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
    return render(request, 'admin_panel/penalty.html')


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
    return render(request, 'admin_panel/show_penalty.html' , context)
    
    




def change_password(request):
    if request.method == 'POST':
        password = request.POST.get('password')
        new_password = request.POST.get('new_password')
        confirm_passsword = request.POST.get('confirm_password')
        
        if new_password != confirm_passsword:
            messages.success(request, 'New and Confirm password must be same. 😡')
            return redirect('/accounts/change_password/')
        
        user = authenticate(username=request.user.username,password=password)
        if user is None:
            messages.success(request, 'Your old Password is wrong. 😤')
            return redirect('/accounts/change_password/')
        
        raw_user = User.objects.get(id = request.user.id)
        raw_user.set_password(new_password)
        raw_user.save()
        
        login(request,raw_user)
        
        messages.success(request, 'Your password changed! 😇')
        return redirect('/paneladmin/change_password/')
    return render(request , 'admin_panel/change_password.html')
    
