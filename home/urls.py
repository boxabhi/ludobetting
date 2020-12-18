
from django.urls import path,include
from .views import *

urlpatterns = [
    path('' , home ,  name="home"),
    path('history' , history , name="history"),
    path('top-winners' , top_winners , name="top_winners"),
    path('terms-conditions' , terms , name="terms"),
    path('help' , help , name="help"),
    path('howtoplay' , howtoplay , name="howtoplay"),
    
    
]
