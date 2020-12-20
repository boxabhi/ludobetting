
from django.urls import path,include
from .views import *

urlpatterns = [

        path('' , index , name="adminhome"),

        
        path('users/' , userlist , name="userlists"),
        path('user/<profile_id>/show/' , viewuser , name="user_details"),
        path('disputes/' , disputesgame , name="disputegame"),
        path('view/<disputed_id>/disputed/' , viewdisputes , name="view_disputes"),
        path('sellcoinsrequest/' , sellcoinsrequest , name="sellcoinsrequest"),
        path('paycoins/' , paycoins , name="paycoins"),
        path('penalty/' , penalty , name="penalty"),
        path('show_penalty/' , show_penalty,name='show_penalty'),
        
        path('order_coins/' , total_purchase  , name="order_coins"),
        path('change_password/' , change_password , name="admin_change_password")
 
]
