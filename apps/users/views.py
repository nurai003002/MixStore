from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate as auth_login
from django.contrib.auth import login, authenticate
from django.contrib.auth.hashers import make_password
from django.contrib import messages
from django.http import JsonResponse
from django.contrib.auth import logout

from apps.settings.models import Setting
from apps.cart.models import Cart
from apps.users.models import User
# Create your views here.

def register(request):
    setting = Setting.objects.latest('id')
    cart_items = Cart.objects.all()
    cart_items_count = cart_items.count()
    if request.method == "POST":
        if 'register_button' in request.POST:
            username = request.POST.get('username')
            email = request.POST.get('email')
            password = request.POST.get('password')
            confirm_password = request.POST.get('confirm_password')

            errors = {}

            if not username :
                errors['fields'] = 'All fields must be filled.'

            if password != confirm_password:
                errors['password'] = 'Passwords must match.'

            if User.objects.filter(username=username,).exists():
               errors['username'] = 'Имя пользователя уже занято, выберите другое'

            if errors:
               return render(request, 'users/register.html', locals())  
            user = User(username=username,email=email, password=make_password(password))
            user.password = make_password(password)
            user.save()
            # login(request, user)
        return redirect('index') 

    return render(request, 'users/register.html', locals())

def login1(request):
    setting = Setting.objects.latest('id')
    cart_items = Cart.objects.all()
    cart_items_count = cart_items.count()
    if request.method == "POST":
        if 'login_button' in request.POST:
            username = request.POST.get('username')
            password = request.POST.get('password')
            user = authenticate(request, username=username, password=password)

            if user is not None:
                login(request, user)
                return redirect('/')
            else:
                messages.error(request, 'Вы ввели неверные данные')

    return render(request, 'users/login.html', locals())

def user_logout(request):
    logout(request)
    return redirect('/')