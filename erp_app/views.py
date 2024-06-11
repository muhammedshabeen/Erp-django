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
from .decrorator import restrict_access
from django.utils.decorators import method_decorator
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.views.generic import View




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
@restrict_access(user_types=['HR', 'GM'])
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
@restrict_access(user_types=['HR', 'GM'])
def home_page(request):
    return render(request,'home_page.html')

def dashboard(request):
    return render(request,'dashboard.html')

def sample(request):
    return render(request,'layouts-without-navbar.html')

def tables(request):
    return render(request,'tables-basic.html')

@login_required
@restrict_access(user_types=['HR', 'GM'])
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
@restrict_access(user_types=['HR', 'GM'])
def add_user(request):
    context = {}
    if request.method == 'POST':
        form=UserForm(request.POST,request.FILES)
        form1 = UserProfileForm(request.POST)
        print("qqqqqqqqqqqqq")
        if form.is_valid() and form1.is_valid():
            print("enter to the valid")
            user = form.save(commit=False)  # Don't save to the database yet
            user.password = make_password(form.cleaned_data['password'])  # Hash the password
            user.save() 
            user_profile = form1.save(commit=False)
            user_profile.user = user
            user_profile.save()
            messages.success(request,'User added succesfully')
            return redirect('user_view')
        else:
            print("valid ELSE")
            for field_name, errors in form.errors.items():
                for error in errors:
                    messages.error(request, "{}: {}".format(field_name, error))
            for field_name, errors in form1.errors.items():
                for error in errors:
                    messages.error(request, "{}: {}".format(field_name, error))
        context['form'] = UserForm(request.POST,request.FILES)
        context['form1'] = UserProfileForm(request.POST)
        return render(request,'user/create.html',context)
    else:
        context['form'] = UserForm()
        context['form1'] = UserProfileForm()
        return render(request,'user/create.html',context)
    
@login_required
@restrict_access(user_types=['HR', 'GM'])
def edit_user(request,pk):
    context = {}
    user = UserModel.objects.get(id=pk)
    user_profile = UserProfile.objects.get(user=user)
    form = UserForm(instance=user)
    form1 = UserProfileForm(instance=user_profile)
    if request.method == 'POST':
        form = UserForm(request.POST,request.FILES,instance=user)
        form1 = UserProfileForm(request.POST,instance=user_profile)
        if form.is_valid() and form1.is_valid():
            form.save()
            form1.save()
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
    context['form1'] = form1
    return render(request,'user/edit.html',context)


@login_required
@restrict_access(user_types=['HR', 'GM'])
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
@restrict_access(user_types=['HR', 'GM'])
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

@login_required
@restrict_access(user_types=['HR', 'GM'])
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
    
@login_required
@restrict_access(user_types=['HR', 'GM'])
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


@login_required
@restrict_access(user_types=['HR', 'GM'])
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
@restrict_access(user_types=['HR', 'GM'])
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
@restrict_access(user_types=['HR', 'GM'])
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
@restrict_access(user_types=['HR', 'GM'])
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
@restrict_access(user_types=['HR', 'GM'])
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
@restrict_access(user_types=['HR', 'GM'])
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
@restrict_access(user_types=['HR', 'GM'])
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
@restrict_access(user_types=['HR', 'GM'])      
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
@restrict_access(user_types=['HR', 'GM'])
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
    
           
@login_required
@restrict_access(user_types=['HR', 'GM'])
def notes(request):
    context = {}
    notes = Notes.objects.filter(user=request.user).order_by('-id')
    note_filter = NoteFilter(request.GET, queryset=notes)
    paginator = Paginator(note_filter.qs, 7)

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context['page_obj'] = page_obj
    context['note_filter'] = note_filter
    return render(request,'notes/view.html',context)

@login_required
@restrict_access(user_types=['HR', 'GM'])
def create_note(request):
    context = {}
    form = NoteForm()
    if request.method == 'POST':
        form = NoteForm(request.POST,request.FILES)
        print("lll",request.POST,request.FILES)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.user = request.user
            instance.save()
            messages.success(request,"Notes added successfully")
            return redirect('notes')
        else:
            for field_name, errors in form.errors.items():
                for error in errors:
                    messages.error(request, "{}".format(error))
            form = NoteForm(request.POST)
            context['form'] = form
            return render(request,'notes/create.html',context)
    context['form'] = form
    return render(request,'notes/create.html',context)

@login_required
@restrict_access(user_types=['HR', 'GM'])
def edit_note(request,pk):
    context = {}
    note = Notes.objects.get(id=pk)
    form = NoteForm(instance = note)
    if request.method == 'POST':
        form = NoteForm(request.POST,request.FILES,instance=note)
        if form.is_valid():
            print("form",request.POST,request.FILES)
            form.save()
            messages.success(request,"Note edited succesfully")
            params = request.GET.copy()
            redirect_url = reverse('notes')
            if params:
                redirect_url += '?' + params.urlencode()
                return redirect(redirect_url)
            return redirect(redirect_url)
        else:
            for field_name, errors in form.errors.items():
                for error in errors:
                    messages.error(request, "{}".format(error))
    context['form'] = form
    return render(request,'notes/edit.html',context)

@login_required
@restrict_access(user_types=['HR', 'GM'])
def delete_note(request,pk):
    params = request.GET.copy()
    redirect_url = reverse('notes')
    try:
        note = Notes.objects.get(id=pk)
        note.delete()
    except Notes.DoesNotExist:
        messages.error(request,"Note Found")
    if params:
        redirect_url += '?' + params.urlencode()
        return redirect(redirect_url)
    return redirect(redirect_url)


@login_required
@restrict_access(user_types=['HR', 'GM'])
def account_settings(request):
    errors = {}
    context = {}
    user_profile = UserProfile.objects.get(user_id=request.user.id)
    if request.method == 'POST':
        password = request.POST.get('password')
        password_confirm = request.POST.get('password_confirm')
        if not password:
            errors['password'] = 'Password is required.'
            messages.error(request,'Password is required')
        if not password_confirm:
            errors['password_confirm'] = 'Password confirmation is required.'
            messages.error(request,'Password confirmation is required.')
        if password and password_confirm and password != password_confirm:
            errors['password_confirm'] = 'Passwords do not match.'
            messages.error(request,'Passwords do not match')
        if not errors:
            try:
                pass_user = UserModel.objects.get(id=request.user.id) 
                pass_user.password = make_password(password_confirm)
                pass_user.save()
                messages.success(request,'Password changed succesfully!! Please Login')
                
            except UserModel.DoesNotExist:
                messages.error("something went wrong try again later")
        return redirect('account_settings')  # Replace with your success URL
    context['user'] = user_profile
    return render(request,'profile/acount_profile.html',context)




@login_required
@restrict_access(user_types=['HR', 'GM'])
def LeaveRequestListView(request):
    context = {}
    leaves = LeaveRequest.objects.all().order_by('-id')
    leave_filter = LeaveRequestFilter(request.GET, queryset=leaves)
    paginator = Paginator(leave_filter.qs, 7)

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context['page_obj'] = page_obj
    context['leave_filter'] = leave_filter
    return render(request,'leave_request_user/leaverequest_list.html',context)


@login_required
@restrict_access(user_types=['HR', 'GM'])
def approve_leave(request,pk):
    try:
        leave = LeaveRequest.objects.get(id=pk)
        leave.status = 'Active'
        leave.save()
        messages.success(request,'Leave Approved succesfully')
    except LeaveRequest.DoesNotExist:
        messages.error(request,'Leave request doesnot exist')
    params = request.GET.copy()
    redirect_url = reverse('leave_requests')
    if params:
        redirect_url += '?' + params.urlencode()
        return redirect(redirect_url)
    return redirect(redirect_url)
