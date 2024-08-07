from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate as auth_login
from django.contrib.auth import login, authenticate
from django.contrib.auth.hashers import make_password
from django.contrib import messages
from django.http import JsonResponse, HttpResponse
from django.contrib.auth import logout
from apps.telegram_bot.views import get_text
from django.contrib.auth.decorators import login_required
import requests

from apps.settings.models import Setting
from apps.cart.models import CartItem
from apps.products.models import Product, Category
from apps.users.models import User
from apps.billings.models import Billings, BillingProduct
# Create your views here.
@login_required(login_url='/users/register/') 
def checkout(request):
    setting = Setting.objects.latest('id')
    products = Product.objects.all()
    categories = Category.objects.all()
    cart_items = CartItem.objects.all()
    total_price = sum([cart_items.total for cart_items in cart_items])
    cart_items_count = cart_items.count()
    cart_products = CartItem.objects.all()
    
    if request.method == "POST":
        if 'checkout_form' in request.POST:
            # Извлечение данных из формы
            first_name = request.POST.get('first_name')
            last_name = request.POST.get('last_name')
            phone = request.POST.get('phone')
            address = request.POST.get('address')
            city = request.POST.get('city')
            
            # Создание записи в БД для контакта
            try:
                page_contact = Billings.objects.create(
                    first_name=first_name,
                    last_name=last_name,
                    address=address,
                    phone=phone,
                    city=city
                )
            except Exception as e:
                print(f"Ошибка при создании контакта: {e}")
                return HttpResponse("Ошибка при создании заказа.", status=500)

            cart_products = request.session.get('cart', [])
            
            if not cart_products:
                print("Корзина пуста или не существует в сессии")
                return HttpResponse("Корзина пуста.", status=400)

            items_text = ""
            for cart_product in cart_products:
                try:
                    product = Product.objects.get(id=cart_product['product_id'])
                    BillingProduct.objects.create(
                        product=product,
                        quantity=cart_product['quantity'],
                        price=product.price,  # Убедитесь, что поле price существует в модели Product
                        billing=page_contact  # Связь с Billing
                    )
                    items_text += f"{product.title} - {cart_product['quantity']} шт. по цене {product.price} каждый\n"
                except Product.DoesNotExist:
                    items_text += f"Неизвестный продукт: {cart_product['product_id']}\n"

            # Сообщение для отправки в Telegram
            message = f"""
    Оставлена заявка на заказ 🛵
                        
    Имя пользователя: {first_name}
    Адрес: {address}
    Номер телефона: {phone}
    Город: {city}
            
Товары:\n
{items_text}
    """
            send_telegram_message(message)
            
            # Очистка корзины
            print("Очищаем корзину в сессии")
            try:
                del request.session['cart']
                request.session.modified = True
                print("Корзина успешно очищена")
            except KeyError:
                print("Корзина не найдена в сессии")
            return redirect('confirm')
    return render(request, 'user/checkout.html', locals())

def send_telegram_message(message):
    bot_token = '7409456892:AAGNoJmrIyX6_QHmsjv42fQVPnSMJLuW_wQ'
    chat_id = '6564825140'
    url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
    payload = {
        'chat_id': chat_id,
        'text': message,
        'parse_mode': 'HTML'
    }
    response = requests.post(url, data=payload)
    if response.status_code != 200:
        print(f"Ошибка при отправке сообщения в Telegram: {response.text}")
    else:
        print("Сообщение успешно отправлено в Telegram")

def register(request):
    setting = Setting.objects.latest('id')
    cart_items = CartItem.objects.all()
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
    cart_items = CartItem.objects.all()
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

def confirm(request):
    setting = Setting.objects.latest('id')
    cart_items = CartItem.objects.all()
    cart_items_count = cart_items.count()
    return render(request, 'user/confirm.html', locals())
