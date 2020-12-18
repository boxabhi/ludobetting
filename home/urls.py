
from django.urls import path,include
from .views import *

urlpatterns = [
    path('' , landing ,  name="landing"),
    path('user/<username>/' , home ,  name="home"), 
    path('history' , history , name="history"),
    path('top-winners' , top_winners , name="top_winners"),
    
    path('error' , error , name="error"),
    path('success' , success , name="success")
]
