
from django.urls import path,include
from .views import *

urlpatterns = [

        path('' , games , name="games"),
        path('room/<room_id>' , waiting_room , name="waiting_room"),
        path('api/create_game' , create_game , name="create_game"),
        
 
]
