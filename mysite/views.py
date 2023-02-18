from django.shortcuts import render
from django.urls import reverse
from django.http import HttpResponse, HttpResponseRedirect
from .models import UserInfo, UserLevel, UserWallet
import datetime
from .utils import *
from .db_utils import *
import time

def homepage(request):
    return render(request, 'homepage.html')

def login(request):
    content = {}
    # user has clicked the button to log in
    if request.method == 'POST':
        email_or_phone = request.POST.get('username')
        password = request.POST.get('password')
        if not email_or_phone or not password:
            content['error'] = 'Please enter both username and password'
            return render(request, 'login.html', content)
        obj = find_user_by_email_or_phone(email_or_phone)
        if obj == None:
            content['error'] = 'Email or phone number does not exist, please double check or register first!'
            content['show_register'] = True
            return render(request, 'login.html', content)
        
        if obj.password != password:
            content['error'] = 'Password does not match, please double check!'
            return render(request, 'login.html', content)
        
        # update the user's login information
        obj.has_logged_in = True
        obj.logged_in_at = datetime.now()
        obj.logged_in_ip = get_login_ip(request)
        obj.save()
        return HttpResponse('You have logged in successfully')

    return render(request, 'login.html', content)

def register(request):
    content = {}
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        birthday = request.POST.get('birthday')
        if not username or not password or not first_name or not last_name or not birthday:
            content['error'] = 'Please fill out all the fields'
            return render(request, 'register.html', content)

        if find_user_by_email_or_phone(username) != None:
            content['error'] = 'Username already exists, please choose another one or login instead!'
            content['show_login'] = True
            return render(request, 'register.html', content)
        if '@' in username:
            obj = UserInfo(email=username, password=password, first_name=first_name, last_name=last_name, birthday=birthday, created_at=datetime.now())
        else:
            obj = UserInfo(phone_number=username, password=password, first_name=first_name, last_name=last_name, birthday=birthday, created_at=datetime.now())
        obj.save()
        content['prelog'] = "Congratulations! You have successfully registered. Please log in to continue."
        return render(request, 'redirect_to_login.html', content)

    return render(request, 'register.html')