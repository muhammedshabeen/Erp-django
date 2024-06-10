from django import forms
from .models import *
from erp_app.models import *


class PlannedTaskForm(forms.ModelForm):
    class Meta:
        model = PlannedTask
        fields = ['project_name','main_task','sub_task','description','time']
    
        
    def __init__(self, *args, **kwargs):
        super(PlannedTaskForm, self).__init__(*args, **kwargs)
        for name in self.fields.keys():
            self.fields[name].widget.attrs.update({'class':'form-control'})
        
class LeaveRequestForm(forms.ModelForm):
    class Meta:
        model = LeaveRequest
        fields = ['leave_type','date_from','date_to','no_of_days','description']
        widgets = {
            'date_from': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'date_to': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
        }
    def __init__(self, *args, **kwargs):
        super(LeaveRequestForm, self).__init__(*args, **kwargs)
        for name in self.fields.keys():
            self.fields[name].widget.attrs.update({'class':'form-control'})
            
    