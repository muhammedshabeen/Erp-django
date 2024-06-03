from django.urls import path
from .views import *

urlpatterns = [
    
    path('',user_home_page,name='user_home_page'),
    path('user_signin_page',user_signin_page,name='user_signin_page'),
    path('logout-view-user',logout_view_user,name='logout_view_user'),
    
    
]