from django.shortcuts import render, redirect
from .helpers import *
from accounts.models import *
from .models import *
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from datetime import datetime, timedelta
from home.helpers import set_coins
from django.views.decorators.csrf import csrf_exempt
# Create your views here.


@login_required(login_url='/accounts/login/')
def buy_coins(request):
    if request.user.is_authenticated:
        set_coins(request)
        
    if request.method == "POST":
        amount = request.POST.get("amount")
        if amount is None:
            messages.success(request, 'Amount is required 😒')
            
        checkout = {}
        order_id = random_string_generator()
        profile = Profile.objects.filter(user= request.user).first()
        result = make_payment(order_id , amount , request.user.username  , str(profile.whatsapp) ,   "s")
        checkout = {'signature': result , 'orderAmount' : amount , 'orderId' : order_id ,'customerName' :request.user.username , 'customerPhone' :str(profile.whatsapp) }
        context = {'checkout': checkout}
        
        order_coins = OrderCoins(order_id= order_id , user = request.user , amount=amount)
        order_coins.save()
        return render(request,'transaction/buy_coins.html' , context)
        
    return render(request,'transaction/buy_coins.html')

@login_required(login_url='/accounts/login/')
def sell_coins(request):
    if request.user.is_authenticated:
        set_coins(request)
    user = request.user
    if request.method == "POST":
        profile = Profile.objects.filter(user=user).first()
        amount = request.POST.get('amount')
        payment_mode = request.POST.get('payment_method')
        number = request.POST.get('number')
        
        
        if int(amount) > int(profile.coins):
            messages.success(request, "You don't have enough coins 😒")
            return redirect('/transaction/sell-coins/')
            
        if int(amount) < 100:
            messages.success(request, "Amount must be greator than 100 😒")
            return redirect('/transaction/sell-coins/')
            
            
                
            
        total_requests = SellCoins.objects.filter(user=user,created_at__gte = datetime.now() - timedelta(days=1) , is_paid=False)
        
        if len(total_requests) >= 2:
            messages.success(request, "Only two requests per day 😳")
            return redirect('/transaction/sell-coins/')
        
        profile = Profile.objects.filter(user = user).first()
        profile.coins = profile.coins - int(amount)
        profile.save()
        sell_coins_obj = SellCoins(user = user , amount=amount , payment_mode=payment_mode,number=number)
        sell_coins_obj.save()
        messages.success(request, "Your request has been received 🤑")
        return redirect('/transaction/sell-coins/')
         
    pending_requests = SellCoins.objects.filter(user = user , is_paid=False)
    context = {'pending_requests': pending_requests} 
    return render(request,'transaction/sell_coins.html', context)




@csrf_exempt
def payment_success(request):
    data  = (request.body)
    
    
    decode_data = data.decode("utf-8") 
    raw_data = decode_data.split("&")
    order_id = raw_data[0].split("=")
    order_amount = raw_data[1].split('=')
    transaction_status = raw_data[3].split("=")
    
    order_coins = OrderCoins.objects.filter(order_id=order_id[1]).first()
    if transaction_status[1] == 'SUCCESS':
        profile = Profile.objects.filter(user=order_coins.user).first()
        profile.coins += int(float((order_amount[1])))
        profile.save()
        order_coins.status = True
        order_coins.save()
        return redirect('/success')
    return redirect('/error')