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
            messages.success(request, 'User not found')
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
                messages.success(request, 'Wrong Password')
                return redirect('/accounts/login/')
        except User.DoesNotExist:
            return redirect('/error')
    return render(request , 'accounts/login.html')


def register_attempt(request):
    if request.method == "POST":
        username = request.POST.get("username")
        whatsapp = request.POST.get("whatsapp")
        password = request.POST.get("password")
        
        user_by__username = User.objects.filter(username=username).first()
        user_by__whatsapp = Profile.objects.filter(whatsapp = whatsapp).first()
        
        if user_by__username:
            messages.success(request, 'Username is taken')
            return redirect('/accounts/login/')
            
        if user_by__whatsapp:
            messages.success(request, 'Whatsapp number is taken')
            return redirect('/accounts/login/')
        
        
        user = User(username = username)
        user.set_password(password)
        user.save()
        otp = send_otp(whatsapp)
        profile = Profile(whatsapp = whatsapp , user = user , otp=otp)
        profile.save()
        
        user_id = user.id
        return redirect('/accounts/verify_otp/'+ str(user_id))
        
    return render(request , 'accounts/register.html')


def otp_attempt(request , user_id):
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
        confirm_passsword = request.POST.get('confirm_passsword')
        
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
    return render(request, 'account/forget_password.html')






def logout_attempt(request):
    logout(request)
    return redirect('/')