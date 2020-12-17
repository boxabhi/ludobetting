
from django.urls import path,include
from .views import *

urlpatterns = [
    path('login/' , login_attempt ,  name="login"),
    path('register/' , register_attempt ,  name="register"),
    path('logout/' , logout_attempt ,  name="logout"),
    path('verify_otp/<user_id>/' , otp_attempt , name="otp_attempt"),
    path('forget_password_attempt/' , forget_password_attempt , name="forget_password_attempt"),
    path('edit_profile/' , edit_profile , name="edit_profile"),
    path('change_password/' , change_password , name="change_password")
    
    
]
