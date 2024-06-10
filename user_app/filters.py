import django_filters
from erp_app.models import *
from django import forms
from .models import *



class LeaveFilter(django_filters.FilterSet):
    user = django_filters.ModelChoiceFilter(
        queryset=UserModel.objects.all().exclude(is_superuser=True),
        field_name='user',
        label='User',
        widget=forms.Select(attrs={'class': 'form-control'})  # Ensures dropdown styling
    )

    leave_type = models.CharField(null=True,blank=True,max_length=40,choices=(
        ('Casual Leave','Casual Leave'),
        ('Sick Leave','Sick Leave'),
        ('Previlage Leave','Previlage Leave'),
        ('Maintanace Leave','Maintanace Leave'),
        ('Earned Leave','Earned Leave'),
        ('Maternity Leave','Maternity Leave'),
        ('Study Leave or Sabbatical','Study Leave or Sabbatical'),
        ('Quarantine Leave','Quarantine Leave'),
        ('L O P','L O P'),
        ('Compensatry Leave','Compensatry Leave'),
    ))
    status = models.CharField(null=True,blank=True,max_length=40,choices=(
        ('Active','Active'),
        ('Inactive','Inactive'),
    ))

    class Meta:
        model = LeaveRequest
        fields = ['leave_type', 'user', 'status']

    def __init__(self,*args,**kwargs):
        super(LeaveFilter,self).__init__(*args,**kwargs)
        for name in self.filters.keys():
            self.filters[name].field.widget.attrs.update({'class':'form-control','style':'height:41px; padding:0px; padding-left:7px'})
            