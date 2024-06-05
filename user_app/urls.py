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
    path('planned-task',view_create_planned_task,name='view_create_planned_task'),
    path('edit-planned-task/<int:pk>',edit_planned_task,name='edit_planned_task'),
    path('delete-planned-task/<int:pk>',planned_task_delete,name='planned_task_delete'),
    
    
    #NoteUser
    path('view-notes-user',user_notes,name='user_notes'),
    path('create-notes-user',user_create_note,name='user_create_note'),
    path('edit-notes-user/<int:pk>',user_edit_note,name='user_edit_note'),
    path('delete-notes-user/<int:pk>',user_delete_note,name='user_delete_note'),
    
    
    #AjaxPath
    path('ajax/load-main-tasks/', load_main_tasks, name='load_main_tasks'),
    path('ajax/load-sub-tasks/', load_sub_tasks, name='load_sub_tasks'),
    
]