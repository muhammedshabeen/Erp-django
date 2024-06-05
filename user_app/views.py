from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from django.shortcuts import redirect, render
from .models import *
from .forms import *
from django.contrib import messages
from django.core.paginator import Paginator
from django.http import HttpResponse, QueryDict
from django.urls import reverse
from django.contrib.auth import authenticate, login,logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.hashers import make_password
import random,math
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from core import settings
from .decorator import *
from django.views.decorators.csrf import csrf_exempt
from datetime import datetime, timedelta,timezone
from erp_app.models import Notes
from erp_app.forms import NoteForm
from erp_app.filters import NoteFilter



@custom_login_required
def user_home_page(request):
    context = {}
    today_date = datetime.today().strftime('%Y-%m-%d')
    context['start_time'] = None
    context['user_punchin'] = None
    try:
        user_punchin = Attendance.objects.get(date=today_date,user=request.user)
        start_time = {
        "punch_in":user_punchin.punch_in_time if user_punchin else None,
        "lunch_in":user_punchin.lunch_in_time if user_punchin else None,
        "lunch_end":user_punchin.lunch_out_time if user_punchin else None,
        "punch_end":user_punchin.punch_out_time if user_punchin else None,
        }
        context['start_time'] = start_time if start_time else None
        context['user_punchin'] = user_punchin if user_punchin else None
    except Attendance.DoesNotExist:
        pass
    return render(request,'home/home_page.html',context)





def user_signin_page(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        print("POST METHOD",email,password)
        user = authenticate(request, username=email, password=password)
        print("USER IS",user)
        if user is not None:
            if user.status == 'Active' and user.user_type in ['GM','HR','HR']:
                login(request, user)
                next_url = request.POST.get('next', 'home_page')
                return redirect(next_url)
            elif user.status == 'Active' and user.user_type == 'Employer':
                login(request, user)
                next_url = request.POST.get('next', 'user_home_page')
                return redirect(next_url)
            else:
                messages.error(request, 'Invalid email or password.')
                return render(request, 'authentication/user_signin.html')
        else:
            messages.error(request, 'Invalid email or password.')
            return render(request, 'authentication/user_signin.html')
    return render(request,'authentication/user_signin.html')


custom_login_required
def logout_view_user(request):
    logout(request)
    return redirect('user_signin_page')


custom_login_required
def punch_in(request):
    user = request.user
    today_date = datetime.now().strftime('%Y-%m-%d')
    current_time_str = datetime.now().strftime('%H:%M:%S')

    try:
        if not Attendance.objects.filter(user=user, date=today_date).exists():
            Attendance.objects.create(user=user, date=today_date, punch_in_time=current_time_str)
            messages.success(request, "Punch In success")
        else:
            messages.error(request, "Already Punch In")
    except UserModel.DoesNotExist:
        messages.error(request, "User does not exist")
    
    return redirect('user_home_page')



@custom_login_required
def lunch_in(request):
    user = request.user
    today_date = datetime.now().strftime('%Y-%m-%d')
    current_time_str = datetime.now().strftime('%H:%M:%S')
    try:
        lunch_in = Attendance.objects.get(user=user, date=today_date)
        if lunch_in:
            if PlannedTask.objects.filter(user=user,date=today_date).exists():
                lunch_in.lunch_in_time = current_time_str
                lunch_in.save()
                messages.success(request, "Lunch start success")
            else:
                messages.error(request, "Please add the planned task") 
                return redirect('view_create_planned_task')    
        else:
            messages.error(request, "An error occured")
    except Attendance.DoesNotExist:
        messages.error(request, "Please punch in !!!")
    return redirect('user_home_page')


@custom_login_required
def lunch_end(request):
    user = request.user
    today_date = datetime.now().strftime('%Y-%m-%d')
    current_time_str = datetime.now().strftime('%H:%M:%S')
    try:
        lunch_out = Attendance.objects.get(user=user, date=today_date)
        if lunch_out:
            lunch_out.lunch_out_time = current_time_str
            lunch_out.save()
            messages.success(request, "Lunch end success")
            redirect('user_home_page')
        else:
            messages.error(request, "An error occured")
            redirect('user_home_page')
    except Attendance.DoesNotExist:
        messages.error(request, "Please Lunch in in !!!")
    return redirect('user_home_page')

@custom_login_required
def punch_out(request):
    user = request.user
    today_date = datetime.now().strftime('%Y-%m-%d')
    current_time_str = datetime.now().strftime('%H:%M:%S')
    try:
        punch_out = Attendance.objects.get(user=user, date=today_date)
        if punch_out:
            punch_out.punch_out_time = current_time_str
            punch_out.save()
            messages.success(request, "Punch Out success")
            redirect('user_home_page')
        else:
            messages.error(request, "An error occured")
            redirect('user_home_page')
    except Attendance.DoesNotExist:
        messages.error(request, "Please Lunch End  !!!")
    return redirect('user_home_page')


@custom_login_required
def punch_out_before(request):
    user = request.user
    today_date = datetime.now().strftime('%Y-%m-%d')
    current_time_str = datetime.now().strftime('%H:%M:%S')
    if PlannedTask.objects.filter(user=user,date=today_date).exists():
        lunch_in.lunch_in_time = current_time_str
        lunch_in.save()
        messages.success(request, "Lunch start success")
    else:
        messages.error(request, "Please add the planned task") 
        return redirect('view_create_planned_task')
    return redirect('user_home_page')


@custom_login_required
def view_create_planned_task(request):
    context = {}
    today_date = datetime.now().strftime('%Y-%m-%d')
    current_time_str = datetime.now().strftime('%H:%M:%S')
    form = PlannedTaskForm()
    if request.method == 'POST':
        form = PlannedTaskForm(request.POST)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.date = today_date
            instance.time = current_time_str
            instance.user = request.user
            instance.save()
            messages.success(request,'Planned task added successfully')
            return redirect('view_create_planned_task')
        else:
            form = PlannedTaskForm(request.POST)
            for field_name, errors in form.errors.items():
                for error in errors:
                    messages.error(request, "{}".format(error))
    context['form'] = form
    tasks = PlannedTask.objects.filter(date=today_date,user=request.user)
    context['tasks'] = tasks if tasks else None
    return render(request,'planned_task/view_add_planned_task.html',context)





           
@custom_login_required
def user_notes(request):
    context = {}
    notes = Notes.objects.filter(user=request.user).order_by('-id')
    note_filter = NoteFilter(request.GET, queryset=notes)
    paginator = Paginator(note_filter.qs, 7)

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context['page_obj'] = page_obj
    context['note_filter'] = note_filter
    return render(request,'home/notes/view.html',context)

@custom_login_required
def user_create_note(request):
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
            return redirect('user_notes')
        else:
            for field_name, errors in form.errors.items():
                for error in errors:
                    messages.error(request, "{}".format(error))
            form = NoteForm(request.POST)
            context['form'] = form
            return render(request,'home/notes/create.html',context)
    context['form'] = form
    return render(request,'home/notes/create.html',context)

@custom_login_required
def user_edit_note(request,pk):
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
            redirect_url = reverse('user_notes')
            if params:
                redirect_url += '?' + params.urlencode()
                return redirect(redirect_url)
            return redirect(redirect_url)
        else:
            for field_name, errors in form.errors.items():
                for error in errors:
                    messages.error(request, "{}".format(error))
    context['form'] = form
    return render(request,'home/notes/edit.html',context)

@custom_login_required
def user_delete_note(request,pk):
    params = request.GET.copy()
    redirect_url = reverse('user_notes')
    try:
        note = Notes.objects.get(id=pk)
        note.delete()
    except Notes.DoesNotExist:
        messages.error(request,"Note Found")
    if params:
        redirect_url += '?' + params.urlencode()
        return redirect(redirect_url)
    return redirect(redirect_url)