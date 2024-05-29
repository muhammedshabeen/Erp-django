from django.shortcuts import redirect, render
from .models import *
from .forms import *
from django.contrib import messages


def index(request):
    return render(request,'index.html')




def signup_page(request):
    return render(request,'signup.html')

def signin_page(request):
    return render(request,'signin.html')

def index1(request):
    return render(request,'index1.html')

def dashboard(request):
    return render(request,'dashboard.html')

def sample(request):
    return render(request,'layouts-without-navbar.html')

def tables(request):
    return render(request,'tables-basic.html')


def user_view(request):
    context = {}
    users = UserModel.objects.filter().exclude(is_superuser=True)
    context['users'] = users
    return render(request,'user/user.html',context)

def add_user(request):
    context = {}
    if request.method == 'POST':
        form=UserForm(request.POST)
        if form.is_valid():
            form.save()
            messages.error(request,'User added succesfully')
        return redirect('user_view')
    else:
        context['form'] = UserForm()
        return render(request,'user/create.html',context)
