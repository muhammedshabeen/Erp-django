from django.http import HttpResponse
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



@custom_login_required
def user_home_page(request):
    return render(request,'home/home_page.html')





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



def forgot_password_user(request):
    if(request.method == "POST"):
        email = request.POST['email']
        try:
            admin_instance = UserModel.objects.get(email=email)
            # print("////////////////////",admin_instance)
        except UserModel.DoesNotExist:
            messages.error(request,'Check the email')
            return redirect(request.META.get('HTTP_REFERER'))  
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
                subject = 'Doob - Forgotten your password '
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

def redirect_url_user(request,email):
    email = email[:-7]
    return render(request,'registration/otp_validate.html',context={'phone' : email})

def otp_validate_user(request):
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
                return redirect('user_signin_page')
            else:
                messages.error(request, 'Passwords do not match')
                return redirect(request.META.get('HTTP_REFERER'))
        
        except UserModel.DoesNotExist:
            messages.error(request, 'Invalid OTP')
            return redirect(request.META.get('HTTP_REFERER'))
    return render(request,'registration/forgot_passwordotp.html')