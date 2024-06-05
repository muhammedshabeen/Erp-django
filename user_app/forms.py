from django import forms
from .models import *


class PlannedTaskForm(forms.ModelForm):
    class Meta:
        model = PlannedTask
        fields = ['project_name','main_task','sub_task','description','time']
    
        
    def __init__(self, *args, **kwargs):
        super(PlannedTaskForm, self).__init__(*args, **kwargs)
        for name in self.fields.keys():
            self.fields[name].widget.attrs.update({'class':'form-control'})
        