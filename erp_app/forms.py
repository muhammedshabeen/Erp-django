from django import forms
from . models import *



class UserForm(forms.ModelForm):
    class Meta:
        model = UserModel
        fields = ['username','email','password','phone','user_type','status']
    
    def __init__(self, *args, **kwargs):
        super(UserForm, self).__init__(*args, **kwargs)
        for name in self.fields.keys():
            self.fields[name].widget.attrs.update({'class':'form-control'})
            
            
class MainTaskForm(forms.ModelForm):
    class Meta:
        model = MainTask
        fields = ['name','status']
    
    def __init__(self, *args, **kwargs):
        super(MainTaskForm, self).__init__(*args, **kwargs)
        for name in self.fields.keys():
            self.fields[name].widget.attrs.update({'class':'form-control'})