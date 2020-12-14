from django.shortcuts import render

# Create your views here.



def home(request):
    return render(request , 'home/index.html')


def history(request):
    return render(request , 'home/history.html')

def top_winners(request):
    return render(request ,'home/top.html')