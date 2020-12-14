from django.shortcuts import render
from accounts.models import *
# Create your views here.


    
    

def home(request):
    if request.user.is_authenticated:
        set_coins(request)
        
    return render(request , 'home/index.html')


def history(request):
    if request.user.is_authenticated:
        set_coins(request)
        
    return render(request , 'home/history.html')

def top_winners(request):
    return render(request ,'home/top.html')