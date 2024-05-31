from django.shortcuts import redirect, render
from .models import *
from .forms import *
from django.contrib import messages
from django.core.paginator import Paginator
from .filters import *
from django.http import QueryDict
from django.urls import reverse





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
    user_list = UserModel.objects.filter().exclude(is_superuser=True).order_by('-id')
    user_filter = UserFilter(request.GET, queryset=user_list)
    paginator = Paginator(user_filter.qs, 7)

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context['page_obj'] = page_obj
    context['user_filter'] = user_filter
    return render(request,'user/user.html',context)

def add_user(request):
    context = {}
    if request.method == 'POST':
        form=UserForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request,'User added succesfully')
            return redirect('user_view')
        else:
           for field_name, errors in form.errors.items():
                for error in errors:
                    messages.error(request, "{}".format(error))
        context['form'] = UserForm(request.POST)
        return render(request,'user/create.html',context)
    else:
        context['form'] = UserForm()
        return render(request,'user/create.html',context)
    
    
def edit_user(request,pk):
    context = {}
    user = UserModel.objects.get(id=pk)
    form = UserForm(instance=user)
    if request.method == 'POST':
        form = UserForm(request.POST,instance=user)
        if form.is_valid():
            form.save()
            params = request.GET.copy()
            redirect_url = reverse('user_view') 
            messages.success(request,"User edited successfully")
            if params:
                redirect_url += '?' + params.urlencode()
                return redirect(redirect_url)
            return redirect(redirect_url)
        else:
            for field_name, errors in form.errors.items():
                for error in errors:
                    messages.error(request, "{}".format(error))
    context['form'] = form
    return render(request,'user/edit.html',context)



def delete_user(request,pk):
    try:
        user = UserModel.objects.get(id=pk)
        user.delete()
    except UserModel.DoesNotExist:
        messages.info(request,"User doesnot exist")
    
    params = request.GET.copy()
    redirect_url = reverse('user_view') 
    messages.success(request,"User deleted successfully")
    if params:
        redirect_url += '?' + params.urlencode()
        return redirect(redirect_url)
    return redirect('user_view')



def main_task_view(request):
    context = {}
    user_list = MainTask.objects.all().order_by('-id')
    main_task_filter = MainTaskFilter(request.GET, queryset=user_list)
    paginator = Paginator(main_task_filter.qs, 7)

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context['page_obj'] = page_obj
    context['main_task_filter'] = main_task_filter
    return render(request,'task/main_task/view.html',context)


def add_main_task(request):
    context = {}
    if request.method == 'POST':
        form = MainTaskForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request,'Task addedd successfully')
            return redirect('main_task_view')
        else:
            for field_name, errors in form.errors.items():
                for error in errors:
                    messages.error(request, "{}".format(error))
            context['form'] = UserForm(request.POST)
            return render(request,'task/main_task/create.html',context)
    else:
        form = MainTaskForm()
        context['form'] = form
        return render(request,'task/main_task/create.html',context)   


def edit_main_task(request,pk):
    context = {}
    main_task = MainTask.objects.get(id=pk)     
    form = MainTaskForm(instance=main_task)
    if request.method == 'POST':
        form = MainTaskForm(request.POST,instance=main_task)
        if form.is_valid():
            form.save()
            messages.success(request,"Task edited succesfully")
            params = request.GET.copy()
            redirect_url = reverse('main_task_view') 
            if params:
                redirect_url += '?' + params.urlencode()
                return redirect(redirect_url)
            return redirect(redirect_url)
        else:
            for field_name, errors in form.errors.items():
                for error in errors:
                    messages.error(request, "{}".format(error))
    context['form'] = form
    return render(request,'task/main_task/edit.html',context)



def delete_main_task(request,pk):
    try:
        task = MainTask.objects.get(id=pk)
        task.delete()
    except MainTask.DoesNotExist:
        messages.info(request,"Task doesnot exist")
    params = request.GET.copy()
    redirect_url = reverse('main_task_view') 
    messages.success(request,"Task deleted successfully")
    if params:
        redirect_url += '?' + params.urlencode()
        return redirect(redirect_url)
    return redirect(main_task_view)
    
            
            