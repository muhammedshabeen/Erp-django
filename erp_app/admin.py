from django.contrib import admin
from .models import *
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import gettext_lazy as _
from django.contrib.auth import get_user_model

class CustomUserAdmin(UserAdmin):
    # Specify the fields to display in the list view and their order
    list_display = ('email', 'username','phone','user_type', 'status', 'is_staff', 'is_superuser', 'created_at')
    
    # Specify the default ordering
    ordering = ('-created_at',)  # This will order by created_at in descending order

    # Define the fields to display in the detail view
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal info', {'fields': ('username', 'user_type', 'phone', 'status','otp')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
    )

    # Define the fields to display in the add user form
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'username','phone','user_type', 'status', 'password1', 'password2', 'otp','is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions'),
        }),
    )

    # Search fields
    search_fields = ('email', 'username')
    # Filter options
    list_filter = ('is_staff', 'is_superuser', 'is_active', 'user_type', 'status')
admin.site.register(UserModel, CustomUserAdmin)
admin.site.register(MainTask)
admin.site.register(Task)
admin.site.register(Notification)
admin.site.register(Project)

