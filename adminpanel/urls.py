
from django.urls import path,include
from .views import *

urlpatterns = [

        path('' , index , name="adminhome"),
        path('userlist' , userlist , name="userlists"),
        path('userdetails' , viewuser , name="userdetails"),
        path('disputes' , disputesgame , name="disputegame"),
        path('viewdisputes' , viewdisputes , name="viewdisputes"),
        path('sellcoinsrequest' , sellcoinsrequest , name="sellcoinsrequest"),
        path('paycoins' , paycoins , name="paycoins"),
        path('penalty' , penalty , name="penalty"),
 
]
