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




@custom_login_required
def user_home_page(request):
    context = {}
    today_date = datetime.today().strftime('%Y-%m-%d')
    user_punchin = Attendance.objects.get(date=today_date)
    print("usererererer",user_punchin)
    context['user_punchin'] = user_punchin if user_punchin else None
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