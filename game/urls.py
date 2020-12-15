
from django.urls import path,include
from .views import *

urlpatterns = [

        path('' , games , name="games"),
        path('api/create_game' , create_game , name="create_game")
 
]
