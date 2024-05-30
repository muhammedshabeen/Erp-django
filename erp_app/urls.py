from django.urls import path
from .views import *

urlpatterns = [
    path('',index,name='index'),
    
    path('index1',index1,name='index1'),
    path('dashboard',dashboard,name='dashboard'),
    path('sample',sample,name='sample'),
    path('tables',tables,name='tables'),
    
    path('signup-page',signup_page,name='signup_page'),
    path('signin-page',signin_page,name='signin_page'),
    
    #User
    path('user-view',user_view,name='user_view'),
    path('create-user',add_user,name='add_user'),
    path('edit-user/<int:pk>',edit_user,name='edit_user'),
    path('delete-user/<int:pk>',delete_user,name='delete_user'),
]