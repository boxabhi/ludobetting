from django.shortcuts import render,redirect
from django.contrib import messages
from django.contrib.auth.models import User
from .models import *
from .helpers import send_otp
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required

# Create your views here.


def login_attempt(request):
    if request.method == "POST":
        whatsapp = request.POST.get("whatsapp")
        password = request.POST.get("password")

        user_by__whatsapp = Profile.objects.filter(whatsapp = whatsapp).first()
        
            
        if user_by__whatsapp is None:
            messages.success(request, 'User not found 🧐')
            return redirect('/accounts/login/')
        
        if user_by__whatsapp.is_verified == False:
            print(user_by__whatsapp.id)
            messages.success(request, "Your account is not verified")
            user_id = user_by__whatsapp.user.id
            return redirect('/accounts/verify_otp/'+ str(user_id))
        try:    
            raw_user = User.objects.get(id = user_by__whatsapp.user.id)
            user = authenticate(username=raw_user.username,password=password)
            if user:    
                login(request,user)
                return redirect('/')
            else:
                messages.success(request, 'Wrong Password 🧐')
                return redirect('/accounts/login/')
        except User.DoesNotExist:
            return redirect('/error')
    return render(request , 'accounts/login.html')


def register_attempt(request):
    if request.method == "POST":
        username = request.POST.get("username")
        whatsapp = request.POST.get("whatsapp")
        password = request.POST.get("password")
        reffral_user = request.POST.get("reffral_user")
        username = username.replace(" ", "")
          
        user_by__username = User.objects.filter(username=username).first()
        user_by__whatsapp = Profile.objects.filter(whatsapp = whatsapp).first()
        
        if user_by__username:
            messages.success(request, 'Username is taken')
            return redirect('/accounts/register/')
            
        if user_by__whatsapp:
            messages.success(request, 'Whatsapp number is taken')
            return redirect('/accounts/register/')
        
        reffral_user_obj = None
        if reffral_user:
            reffral_user_obj = Profile.objects.filter(whatsapp=reffral_user).first()
            if reffral_user_obj is None:
                messages.success(request, 'Incorrect Reffral number')
                return redirect('/accounts/register/')

            reffral_user_obj = reffral_user_obj.user
            
            
        
        
        user = User(username = username)
        user.set_password(password)
        user.save()
        otp = send_otp(whatsapp)
        profile = Profile(whatsapp = whatsapp , user = user , otp=otp , referral_by=reffral_user_obj)
        profile.save()
        
        user_id = user.id
        if reffral_user_obj:
            refer_table = ReffralTable(user = reffral_user_obj , refer = user)
            refer_table.save()
        
        return redirect('/accounts/verify_otp/'+ str(user_id))
        
    return render(request , 'accounts/register.html')


def otp_attempt(request , user_id):
    send_again = request.GET.get('send_again', None)
    if send_again:
        user = User.objects.get(id = user_id)
        profile = Profile.objects.filter(user=user).first()
        otp = send_otp(profile.whatsapp)
        profile.otp = otp
        profile.save()
        messages.success(request, 'OTP sent 😎' + profile.whatsapp)
        return redirect('/accounts/verify_otp/'+ str(user_id))            

    
    if request.method == 'POST':
        try:
            user = User.objects.get(id = user_id)
            otp = request.POST.get('otp')
            profile = Profile.objects.filter(user=user).first()
            print(profile)
            if profile.otp == otp:
                profile.is_verified = True
                profile.save()
                messages.success(request, 'Login to you account !  😁')
                return redirect('/accounts/login/')
            else:
                messages.success(request, 'Wrong OTP')
                return redirect('/accounts/verify_otp/'+ str(user_id))            
        except User.DoesNotExist:
            return redirect('/error')
    return render(request , 'accounts/otp.html')


@login_required(login_url='/accounts/login/')
def edit_profile(request):
    if request.method == "POST":
        username = request.POST.get('username')
        
        check_user_name = User.objects.filter(username=username).first()
        if check_user_name:
            messages.success(request, 'Oops! Username already taken 😁')
            return redirect('/accounts/edit_profile/')
        try:
            user = User.objects.get(id= request.user.id)
            user.username = username
            user.save()
            messages.success(request, 'Your username changed! Nice username !  😁')
            return redirect('/accounts/edit_profile')
        except User.DoesNotExist:
            return redirect('/error')
    return render(request , 'accounts/edit_profile.html')

@login_required(login_url='/accounts/login/')
def change_password(request):
    if request.method == "POST":
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
        return redirect('/accounts/change_password/')
        
    return render(request , 'accounts/change_password.html')
 


def forget_password_attempt(request):
   
    
    if request.method == 'POST':
        whatsapp = request.POST.get("whatsapp")
        profile = Profile.objects.filter(whatsapp=whatsapp).first()
        
        if profile is None:
            messages.success(request, 'No account found 😲')
            return redirect('/accounts/forget_password_attempt/')
            
        otp = send_otp(whatsapp)
        profile.otp = otp
        profile.save()
        return redirect('/accounts/forget_password_otp/'+str(profile.id))
    return render(request, 'accounts/forget_password.html')

def forget_password_otp(request , id):
    send_again = request.GET.get('send_again', None)
    if send_again:
        profile = Profile.objects.get(id=id)
        otp = send_otp(profile.whatsapp)
        profile.otp = otp
        profile.save()
        messages.success(request, 'OTP sent 😎' + profile.whatsapp)
        return redirect('/accounts/forget_password_otp/'+str(profile.id))
        
        
    try:
        profile = Profile.objects.get(id = id)
    except Profile.DoesNotExist:
        return redirect('/error')
    
    if request.method == 'POST':
        otp = request.POST.get('otp')
        if otp != profile.otp:
            messages.success(request, 'Incorrect OTP 😲')
            return redirect('/accounts/forget_password_otp/'+str(profile.id))
        else:
            messages.success(request, 'OTP matched 😎')
            return redirect('/accounts/forget_password_change/'+str(profile.id))
            
    return render(request, 'accounts/forget_password_otp.html')
            
            
            
def forget_password_change(request , id):
    if request.method == 'POST':
        password = request.POST.get('password')
        confirm_passsword = request.POST.get('confirm_password')
        print(password)
        print(confirm_passsword)
        if password != confirm_passsword:
            messages.success(request, 'New and Confirm password must be same. 😡')
            return redirect('/accounts/forget_password_change/'+id)
        else:
            try : 
                profile = Profile.objects.get(id = id)
                user = User.objects.get(id = profile.user.id)
                user.set_password(password)
                user.save()
                messages.success(request, 'Your password changed! 😇')
                return redirect('/accounts/login/')
            except Profile.DoesNotExist:
                return redirect('/error')
                
    return render(request, 'accounts/forget_password_change.html')

        
    
        
    


def logout_attempt(request):
    logout(request)
    return redirect('/')