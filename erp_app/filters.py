# filters.py
import django_filters
from .models import *
from django import forms


class UserFilter(django_filters.FilterSet):
    username = django_filters.CharFilter(field_name='username', 
                                         lookup_expr='icontains',
                                         widget=forms.TextInput(attrs={'placeholder': 'Enter username'}))
    email = django_filters.CharFilter(field_name='email',
                                      lookup_expr='icontains',
                                      widget=forms.EmailInput(attrs={'placeholder': 'Enter email'}))
    status = django_filters.ChoiceFilter(choices=(
        ('Active', 'Active'),
        ('Inactive', 'Inactive'),
        ('Deleted', 'Deleted'),
        ('Pending', 'Pending')
    ))

    class Meta:
        model = UserModel
        fields = ['username', 'email', 'status']

    def __init__(self,*args,**kwargs):
        super(UserFilter,self).__init__(*args,**kwargs)
        for name in self.filters.keys():
            self.filters[name].field.widget.attrs.update({'class':'form-control','style':'height:41px; padding:0px; padding-left:7px'})
            
            
class MainTaskFilter(django_filters.FilterSet):
    name = django_filters.CharFilter(field_name='name', 
                                         lookup_expr='icontains',
                                         widget=forms.TextInput(attrs={'placeholder': 'Enter Title'}))
    status = django_filters.ChoiceFilter(choices=(
        ('Active', 'Active'),
        ('Inactive', 'Inactive'),
    ))

    class Meta:
        model = MainTask
        fields = ['name', 'status']

    def __init__(self,*args,**kwargs):
        super(MainTaskFilter,self).__init__(*args,**kwargs)
        for name in self.filters.keys():
            self.filters[name].field.widget.attrs.update({'class':'form-control','style':'height:41px; padding:0px; padding-left:7px'})
            
            

class TaskFilter(django_filters.FilterSet):
    main_task = django_filters.ModelChoiceFilter(
        queryset=MainTask.objects.all(),
        field_name='main_task',
        to_field_name='name',  # Adjust this if you want to filter by a specific field in MainTask
        widget=forms.TextInput(attrs={'placeholder': 'Enter Title'})
    )
    user = django_filters.ModelChoiceFilter(
        queryset=UserModel.objects.all().exclude(is_superuser=True),
        field_name='user',
        label='User',
        widget=forms.Select(attrs={'class': 'form-control'})  # Ensures dropdown styling
    )
    task_status = django_filters.ChoiceFilter(choices=(
        ('Assigned','Assigned'),
        ('In Progress','In Progress'),
        ('Completed', 'Completed'),
        ('On Hold', 'On Hold'),
        ('Cancelled', 'Cancelled'),
        ('Delayed', 'Delayed'),
        ('Under Review', 'Under Review'),
        ('Blocked', 'Blocked'),
    ))
    status = django_filters.ChoiceFilter(choices=(
        ('Active', 'Active'),
        ('Inactive', 'Inactive'),
    ))

    class Meta:
        model = Task
        fields = ['main_task','user','task_status','status']

    def __init__(self,*args,**kwargs):
        super(TaskFilter,self).__init__(*args,**kwargs)
        for name in self.filters.keys():
            self.filters[name].field.widget.attrs.update({'class':'form-control','style':'height:41px; padding:0px; padding-left:7px'})