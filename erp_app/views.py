from django.shortcuts import redirect, render
from .models import *
from .forms import *
from django.contrib import messages
from django.core.paginator import Paginator
from .filters import *
from django.http import HttpResponse, QueryDict
from django.urls import reverse
from django.contrib.auth import authenticate, login,logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.hashers import make_password
import random,math
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string




def index(request):
    return render(request,'index.html')

def signup_page(request):
    return render(request,'signup.html')

def signin_page(request):
    next_url = request.GET.get('next')
    print("next_urlnext_url", next_url)
    
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        user = authenticate(request, username=email, password=password)
        
        if user is not None and user.status == 'Active':
            if user.user_type in ['GM', 'HR']:
                login(request, user)
                return redirect(next_url if next_url else 'home_page')
            elif user.user_type == 'Employer':
                login(request, user)
                return redirect(next_url if next_url else 'user_home_page')
        else:
            messages.error(request, 'Invalid email or password.')
            return render(request, 'signin.html')
    
    return render(request, 'signin.html')

@login_required
def logout_view(request):
    logout(request)
    return redirect('signin_page')



def forgot_password(request):
    if(request.method == "POST"):
        email = request.POST['email']
        try:
            admin_instance = UserModel.objects.get(email=email)
        except UserModel.DoesNotExist:
            print("YYYYYY")
            messages.error(request,'Check the email')
            return redirect(request.META.get('HTTP_REFERER'))  
        print("KKKKKK")
        if admin_instance:
            admin_instance.otp = None
            admin_instance.save()
            
            if(email and admin_instance is not None):
                digits = "0123456789"
                OTP = ""
                for i in range(6) :
                    OTP += digits[math.floor(random.random() * 10)]
                    
                admin_instance.otp = OTP
                admin_instance.save()
                html_message = render_to_string('forgotpassword.html', {'otp': OTP,'image_url':"base_domain_name",'mail':admin_instance.email})
                subject = 'ABC - Forgotten your password '
                sender_email = settings.EMAIL_HOST_USER
                recipient_emails = admin_instance.email

                email_message = EmailMultiAlternatives(
                    subject=subject,
                    body='',
                    from_email=sender_email,
                    to=[recipient_emails],
                )
                email_message.attach_alternative(html_message, 'text/html')
                email_message.send(fail_silently=False)
                return redirect('redirect_url',email=email)
    return render(request,'registration/forgot_passwordotp.html')

def redirect_url(request,email):
    email = email[:-7]
    return render(request,'registration/otp_validate.html',context={'phone' : email})

def otp_validate(request):
    if(request.method == 'POST'):
        reset_otp = request.POST.getlist('reset_otp')
        otp = ' '.join(reset_otp).replace(' ','')
        print("pppppotsss",otp)
        reset_password = request.POST.get('reset_password',None)
        reset_passwordconfirm = request.POST.get('reset_passwordconfirm',None)
        try:
            admin_instance = UserModel.objects.get(otp=otp)
            print("admin_instance", admin_instance)
            
            if reset_password == reset_passwordconfirm:
                admin_instance.password = make_password(reset_passwordconfirm)
                admin_instance.otp = None
                admin_instance.save()
                messages.success(request, 'Password reset successfully')
                return redirect('signin_page')
            else:
                messages.error(request, 'Passwords do not match')
                return redirect(request.META.get('HTTP_REFERER'))
        
        except UserModel.DoesNotExist:
            messages.error(request, 'Invalid OTP')
            return redirect(request.META.get('HTTP_REFERER'))
    return render(request,'registration/forgot_passwordotp.html')

@login_required
def home_page(request):
    return render(request,'home_page.html')

def dashboard(request):
    return render(request,'dashboard.html')

def sample(request):
    return render(request,'layouts-without-navbar.html')

def tables(request):
    return render(request,'tables-basic.html')

@login_required
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

@login_required
def add_user(request):
    context = {}
    if request.method == 'POST':
        form=UserForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)  # Don't save to the database yet
            user.password = make_password(form.cleaned_data['password'])  # Hash the password
            user.save() 
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
    
@login_required
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


@login_required
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



@login_required
def project(request):
    context = {}
    projects = Project.objects.all().order_by('-id')
    project_filter = ProjectFilter(request.GET, queryset=projects)
    paginator = Paginator(project_filter.qs, 7)

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context['page_obj'] = page_obj
    context['project_filter'] = project_filter
    return render(request,'project/view.html',context)

def add_project(request):
    context = {}
    if request.method == 'POST':
        form = ProjectForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request,"Project added successfully")
            return redirect('project')
        else:
            for field_name, errors in form.errors.items():
                for error in errors:
                    messages.error(request, "{}".format(error))
            context['form'] = ProjectForm(request.POST)
            return render(request,'project/create.html',context)
    else:
        context['form'] = ProjectForm()
        return render(request,'project/create.html',context)
    
    
def edit_project(request,pk):
    context = {}
    project = Project.objects.get(id=pk)
    form = ProjectForm(instance = project)
    if request.method == 'POST':
        form = ProjectForm(request.POST,instance = project)
        if form.is_valid():
            form.save()
            messages.success(request,"Project edited succesfully")
            params = request.GET.copy()
            redirect_url = reverse('project')
            if params:
                redirect_url += '?' + params.urlencode()
                return redirect(redirect_url)
            return redirect(redirect_url)
        else:
            for field_name, errors in form.errors.items():
                for error in errors:
                    messages.error(request, "{}".format(error))
    context['form'] = form
    return render(request,'project/edit.html',context)



def delete_project(request,pk):
    try:
        project = Project.objects.get(id=pk)
        project.delete()
    except Project.DoesNotExist:
        messages.error(request,"Project doesnot exist")
    params = request.GET.copy()
    redirect_url = reverse('project')
    if params:
        redirect_url += '?' + params.urlencode()
        return redirect(redirect_url)
    return redirect(redirect_url)   
        



@login_required
def main_task_view(request):
    context = {}
    main_tasks = MainTask.objects.all().order_by('-id')
    main_task_filter = MainTaskFilter(request.GET, queryset=main_tasks)
    paginator = Paginator(main_task_filter.qs, 7)

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context['page_obj'] = page_obj
    context['main_task_filter'] = main_task_filter
    return render(request,'task/main_task/view.html',context)

@login_required
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
            context['form'] = MainTaskForm(request.POST)
            return render(request,'task/main_task/create.html',context)
    else:
        form = MainTaskForm(request.POST)
        context['form'] = form
        return render(request,'task/main_task/create.html',context)   

@login_required
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


@login_required
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
    
            
            
@login_required
def view_task(request):
    context = {}
    sub_tasks = Task.objects.all().order_by('-id')
    sub_task_filter = TaskFilter(request.GET, queryset=sub_tasks)
    paginator = Paginator(sub_task_filter.qs, 7)

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context['page_obj'] = page_obj
    context['sub_task_filter'] = sub_task_filter
    return render(request,'task/sub_task/view.html',context)


@login_required
def add_sub_task(request):
    context = {}
    if request.method == 'POST':
        form = TaskForm(request.POST)
        if form.is_valid():
            instance = form.save()
            try:
                message = f'{request.user.username} added task {instance.main_task.name} to you .'
                Notification.objects.create(recieve_user=instance.user,send_user=request.user,description=message)
            except Exception as e:
                print("wewewewe",e)
            messages.success(request,"Sub task added successfully")
            return redirect('view_task')
        else:
            for field_name, errors in form.errors.items():
                for error in errors:
                    messages.error(request, "{}".format(error))
            context['form'] = TaskForm(request.POST)
            return render(request,'task/sub_task/create.html',context)
    context['form'] = TaskForm()
    return render(request,'task/sub_task/create.html',context)
            
@login_required         
def edit_sub_task(request,pk):
    context = {}
    sub_task = Task.objects.get(id=pk)
    form = TaskForm(instance=sub_task)
    if request.method == 'POST':
        form = TaskForm(request.POST,instance=sub_task)
        if form.is_valid():
            form.save()
            messages.success(request,"Task edited successfully")
            params = request.GET.copy()
            redirect_url = reverse('view_task')
            if params:
                redirect_url += '?' + params.urlencode()
                return redirect(redirect_url)
            return redirect(redirect_url)
        else:
            for field_name, errors in form.errors.items():
                for error in errors:
                    messages.error(request, "{}".format(error))
    context['form'] = form
    return render(request,'task/sub_task/edit.html',context)

@login_required
def sub_task_delete(request,pk):
    try:
        sub_task = Task.objects.get(id=pk)
        sub_task.delete()
    except Task.DoesNotExist:
        messages.info(request,"Task doesnot exist")
    params = request.GET.copy()
    redirect_url = reverse('view_task')
    messages.success(request,"Task deleted succesfully")
    if params:
        redirect_url += '?' + params.urlencode()
        return redirect(redirect_url)
    return redirect(redirect_url)
    
            