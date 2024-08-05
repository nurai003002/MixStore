from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate as auth_login
from django.contrib.auth import login, authenticate
from django.contrib.auth.hashers import make_password
from django.contrib import messages
from django.http import JsonResponse
from django.contrib.auth import logout
from apps.telegram_bot.views import get_text

from apps.settings.models import Setting
from apps.cart.models import Cart, CartItem
from apps.products.models import Product, Category
from apps.users.models import User
from apps.billings.models import Billings
# Create your views here.
def checkout(request):
    setting = Setting.objects.latest('id')
    products = Product.objects.all()
    categories = Category.objects.all()
    cart_items = Cart.objects.all()
    total_price = sum([cart_item.total for cart_item in cart_items])
    cart_items_count = cart_items.count()
    cart_products = CartItem.objects.all()
    if request.method=="POST":
        if 'checkout_form' in request.POST:
            first_name = request.POST.get('first_name')
            email = request.POST.get('email')
            phone = request.POST.get('phone')
            message = request.POST.get('message')
            page_contact = Billings.objects.create(first_name=first_name, email=email, phone=phone, message=message)
            if page_contact:
                get_text(f"""
                Оставлена заявка на обратный звонок 📞
                         
    Имя пользователя:  {first_name}
    Почта: {email}
    Номер телефона: {phone}
    Сообщение: {message}

    """)
    return render(request, 'user/checkout.html', locals())
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

            if not username or not email or not password:
                errors['fields'] = 'All fields must be filled.'

            if password != confirm_password:
                errors['password'] = 'Passwords must match.'

            if User.objects.filter(username=username,).exists():
               errors['username'] = 'Имя пользователя уже занято, выберите другое'

            if User.objects.filter(email=email).exists():
                errors['email'] = 'Email уже занят, введите другой'

            if errors:
               return render(request, 'user/register.html', locals())  
            
            user = User(username=username,email=email, password=make_password(password))
            user.password = make_password(password)
            user.save()
        return redirect('index') 

    return render(request, 'user/register.html', locals())

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

    return render(request, 'user/login.html', locals())

def user_logout(request):
    logout(request)
    return redirect('/')