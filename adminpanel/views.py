from django.shortcuts import render

# Create your views here.




def index(request):
    return render(request, 'admin/admin-home.html')

def userlist(request):
    return render(request, 'admin/userlists.html')

def viewuser(request):
    return render(request, 'admin/viewuser.html')


def disputesgame(request):
    return render(request, 'admin/disputeslist.html')


def viewdisputes(request):
    return render(request, 'admin/viewdisputes.html')

def sellcoinsrequest(request):
    return render(request, 'admin/sellcoinsrequests.html')

def paycoins(request):
    return render(request, 'admin/paycoins.html')

def penalty(request):
    return render(request, 'admin/penalty.html')

