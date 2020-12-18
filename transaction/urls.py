
from django.urls import path,include
from .views import *

urlpatterns = [
    path('buy-coins/' , buy_coins ,  name="buy_coins"),
    path('sell-coins/' , sell_coins ,  name="sell_coins"),
    path('payment_success' , payment_success , name="payment_success")
   
    
]
