
from django.urls import path,include
from .views import *
from transaction.views import payment_success
urlpatterns = [
    path('' , landing ,  name="landing"),
    path('user/<username>/' , home ,  name="home"), 
    path('history' , history , name="history"),
    path('top-winners' , top_winners , name="top_winners"),
    path('terms-conditions' , terms , name="terms"),
    path('help' , help , name="help"),
    path('howtoplay' , howtoplay , name="howtoplay"),
    
    path('error' , error , name="error"),
    path('success' , success , name="success"),
    path('payment_success' , payment_success , name="payment_success"),
    path('api/get_games' , fake_api , name="fake_api"),
    
    path('refer/' ,  refer , name="refer"),
    
]
