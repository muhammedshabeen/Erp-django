from django import forms
from . models import *



class UserForm(forms.ModelForm):
    class Meta:
        model = UserModel
        fields = ['username','email','password','phone','user_type','status']
        widgets = {
            'password': forms.PasswordInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter password',
            })
        }
    
    def __init__(self, *args, **kwargs):
        super(UserForm, self).__init__(*args, **kwargs)
        for name in self.fields.keys():
            self.fields[name].widget.attrs.update({'class':'form-control'})
            
            
class ProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = ['name','status']
    
    def __init__(self, *args, **kwargs):
        super(ProjectForm, self).__init__(*args, **kwargs)
        for name in self.fields.keys():
            self.fields[name].widget.attrs.update({'class':'form-control'})
            
class MainTaskForm(forms.ModelForm):
    class Meta:
        model = MainTask
        fields = ['name','project_name','status']
    
    def __init__(self, *args, **kwargs):
        super(MainTaskForm, self).__init__(*args, **kwargs)
        for name in self.fields.keys():
            self.fields[name].widget.attrs.update({'class':'form-control'})
            

class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['main_task','user','description','task_status','time_duration','status']
    
    def __init__(self, *args, **kwargs):
        super(TaskForm, self).__init__(*args, **kwargs)
        for name in self.fields.keys():
            self.fields[name].widget.attrs.update({'class':'form-control'})
            
            
class NoteForm(forms.ModelForm):
    class Meta:
        model = Notes
        fields = ['content','file']
    
    def __init__(self, *args, **kwargs):
        super(NoteForm, self).__init__(*args, **kwargs)
        for name in self.fields.keys():
            self.fields[name].widget.attrs.update({'class':'form-control'})
    
        