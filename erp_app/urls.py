from django.urls import path
from .views import *

urlpatterns = [
    path('index',index,name='index'),
    
    path('',home_page,name='home_page'),
    path('dashboard',dashboard,name='dashboard'),
    path('sample',sample,name='sample'),
    path('tables',tables,name='tables'),
    
    path('signup-page',signup_page,name='signup_page'),
    path('log-out',logout_view,name='logout_view'),
    path('signin-page',signin_page,name='signin_page'),
    path('forgot-password',forgot_password,name='forgot_password'),
    path('redirect_url/<str:email>',redirect_url,name='redirect_url'),
    path('otp_validate',otp_validate,name='otp_validate'),
    
    
    
    
    #User
    path('user-view',user_view,name='user_view'),
    path('create-user',add_user,name='add_user'),
    path('edit-user/<int:pk>',edit_user,name='edit_user'),
    path('delete-user/<int:pk>',delete_user,name='delete_user'),
    
    
    #Project
    path('view-project',project,name='project'),
    path('create-project',add_project,name='add_project'),
    path('edit-project/<int:pk>',edit_project,name='edit_project'),
    path('delete-project/<int:pk>',delete_project,name='delete_project'),
    
    
    #MainTask
    path('main-task',main_task_view,name='main_task_view'),
    path('add-task',add_main_task,name='add_main_task'),
    path('edit-task/<int:pk>',edit_main_task,name='edit_main_task'),
    path('delete-task/<int:pk>',delete_main_task,name='delete_main_task'),
    
    
    #SubTask
    path('sub-task',view_task,name='view_task'),
    path('create-sub-task',add_sub_task,name='add_sub_task'),
    path('edit-sub-task/<int:pk>',edit_sub_task,name='edit_sub_task'),
    path('delete-sub-task/<int:pk>',sub_task_delete,name='sub_task_delete'),
]