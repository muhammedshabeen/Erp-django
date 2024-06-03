from django.urls import path
from .views import *

urlpatterns = [
    #HomePage
    path('',user_home_page,name='user_home_page'),
    
    #Authentication
    path('user_signin_page',user_signin_page,name='user_signin_page'),
    path('logout-view-user',logout_view_user,name='logout_view_user'),
    
    #PunchIn
    path('punch-in',punch_in,name="punch_in"),
    path('lunch-in',lunch_in,name="lunch_in"),
    path('lunch-end',lunch_end,name="lunch_end"),
    path('punch-out',punch_out,name="punch_out"),
    path('punch-out-before',punch_out_before,name="punch_out_before"),
    
    
    #PlannedTask
    path('planned-task',view_create_planned_task,name='view_create_planned_task')
    
    
    
    
]