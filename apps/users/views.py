from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate as auth_login
from django.contrib.auth import login, authenticate
from django.contrib.auth.hashers import make_password
from django.core.mail import send_mail,BadHeaderError
from django.contrib import messages
from django.http import JsonResponse, HttpResponse
from django.contrib.auth import logout
from apps.telegram_bot.views import get_text
from django.contrib.auth.decorators import login_required
import requests, random
from django.views.decorators.csrf import csrf_exempt
from decimal import Decimal

from apps.settings.models import Setting
from apps.cart.models import CartItem
from apps.products.models import Product, Category
from apps.users.models import User
from apps.billings.models import Billings, BillingProduct
from apps.secondary.models import Subscribe
from apps.users.forms import EmailForm, ResetPasswordForm

# Create your views here.
@login_required(login_url='/user/register/') 
def checkout(request):
    setting = Setting.objects.latest('id')
    products = Product.objects.all()
    categories = Category.objects.all()
    cart_items = CartItem.objects.all()

    cart_items_count = cart_items.count()
    if 'email_send' in request.POST:
            email = request.POST.get('email')
            try:
                # Сохранение email в базе данных
                Subscribe.objects.create(email=email)
                
                # Отправка письма
                send_mail(
                    'Подписка на рассылку',  # Subject
                    f'Ваша почта: {email}\nСпасибо за подписку!',  # Message
                    'noreply@somehost.local',  # From email
                    [email],  # To email
                    fail_silently=False,
                )
                return redirect('contact')
            except BadHeaderError:
                return JsonResponse({'error': 'Invalid header found.'}, status=500)
            except ConnectionRefusedError as e:
                return JsonResponse({'error': f'Connection refused: {e}'}, status=500)

    if request.user.is_authenticated:
        cart_items = CartItem.objects.filter(user=request.user)
    else:
        session_key = request.session.session_key
        cart_items = CartItem.objects.filter(session_key=session_key)

    delivery_cost = 250
    total_price = sum([cart_items.total for cart_items in cart_items])
    if total_price < 1500:
        total_price += delivery_cost  
    else:
        free_delivery = True
    

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

            if not cart_items.exists():
                print("Корзина пуста или не существует в сессии")
                return HttpResponse("Корзина пуста.", status=400)

            items_text = ""
            for cart_product in cart_items:
                BillingProduct.objects.create(
                    product=cart_product.product,
                    quantity=cart_product.quantity,
                    price=cart_product.price,
                    billing=page_contact
                )
                items_text += f"{cart_product.product.title} - {cart_product.quantity} шт. по цене {cart_product.price} каждый\n"
                total_price = Decimal(0)  # Initialize as a Decimal
                for cart_product in cart_items:
                    total_price += cart_product.quantity * cart_product.price  # Ensure this is a numeric operation

                # Convert to string when displaying
                total_price_display = f"{total_price:.2f}"
                
            message = f"""
    Оставлена заявка на заказ 🛵
                        
    Имя пользователя: {first_name}
    Адрес: {address}
    Номер телефона: {phone}
    Город: {city}
            
Товары:
{items_text}

Общая сумма: {delivery_cost+total_price} сомов
вместе с доставкой
    """
            send_telegram_message(message)
            
            cart_items.delete()  
            request.session.flush() 
            
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
    if 'email_send' in request.POST:
            email = request.POST.get('email')
            try:
                # Сохранение email в базе данных
                Subscribe.objects.create(email=email)
                
                # Отправка письма
                send_mail(
                    'Подписка на рассылку',  # Subject
                    f'Ваша почта: {email}\nСпасибо за подписку!',  # Message
                    'noreply@somehost.local',  # From email
                    [email],  # To email
                    fail_silently=False,
                )
                return redirect('contact')
            except BadHeaderError:
                return JsonResponse({'error': 'Invalid header found.'}, status=500)
            except ConnectionRefusedError as e:
                return JsonResponse({'error': f'Connection refused: {e}'}, status=500)
    if request.method == "POST":
        if 'register_button' in request.POST:
            username = request.POST.get('username')
            email = request.POST.get('email')
            password = request.POST.get('password')
            confirm_password = request.POST.get('confirm_password')

            errors = {}

            # Проверка на заполнение всех полей
            if not username or not email or not password:
                errors['fields'] = 'All fields must be filled.'

            # Проверка совпадения паролей
            if password != confirm_password:
                errors['password'] = 'Passwords must match.'

            # Проверка уникальности имени пользователя
            if User.objects.filter(username=username).exists():
                errors['username'] = 'Имя пользователя уже занято, выберите другое.'

            # Проверка уникальности email
            if User.objects.filter(email=email).exists():
                errors['email'] = 'Email уже занят, введите другой.'

            # Если есть ошибки, возвращаем форму с ошибками
            if errors:
                return render(request, 'user/register.html', locals())  

            # Создание нового пользователя
            user = User(username=username, email=email)
            user.password = make_password(password)
            user.save()

            # Перенаправление на главную страницу после успешной регистрации
            return redirect('index') 
    return render(request, 'user/register.html', locals())

def login1(request):
    setting = Setting.objects.latest('id')
    cart_items = CartItem.objects.all()
    if 'email_send' in request.POST:
            email = request.POST.get('email')
            try:
                # Сохранение email в базе данных
                Subscribe.objects.create(email=email)
                
                # Отправка письма
                send_mail(
                    'Подписка на рассылку',  # Subject
                    f'Ваша почта: {email}\nСпасибо за подписку!',  # Message
                    'noreply@somehost.local',  # From email
                    [email],  # To email
                    fail_silently=False,
                )
                return redirect('contact')
            except BadHeaderError:
                return JsonResponse({'error': 'Invalid header found.'}, status=500)
            except ConnectionRefusedError as e:
                return JsonResponse({'error': f'Connection refused: {e}'}, status=500)
    cart_items_count = cart_items.count()
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return JsonResponse({'success': True, 'redirect_url': '/'})  # Перенаправление после успешного логина
        else:
            return JsonResponse({'success': False, 'error': 'Неправильное имя пользователя или пароль'})


    
    return render(request, 'user/login.html', locals())


def user_logout(request):
    logout(request)
    return redirect('/')

@csrf_exempt  # Только для тестирования, удалите в продакшене
def subscribe(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        # Логика для обработки подписки
        if email:
            # Если подписка успешна
            return JsonResponse({"success": True})
        else:
            return JsonResponse({"success": False}, status=400)
    return JsonResponse({"success": False}, status=400)

def confirm(request):
    setting = Setting.objects.latest('id')
    cart_items = CartItem.objects.all()
    cart_items_count = cart_items.count()
    return render(request, 'user/confirm.html', locals())

def forgot_password(request):
    setting = Setting.objects.latest('id')
    cart_items = CartItem.objects.all()
    cart_items_count = cart_items.count()
    if request.method == 'POST':
        if 'email_send' in request.POST:
            email = request.POST.get('email')
            try:
                # Сохранение email в базе данных
                Subscribe.objects.create(email=email)
                
                # Отправка письма
                send_mail(
                    'Подписка на рассылку',  # Subject
                    f'Ваша почта: {email}\nСпасибо за подписку!',  # Message
                    'noreply@somehost.local',  # From email
                    [email],  # To email
                    fail_silently=False,
                )
                return redirect('forgot_password')
            except BadHeaderError:
                return JsonResponse({'error': 'Invalid header found.'}, status=500)
            except ConnectionRefusedError as e:
                return JsonResponse({'error': f'Connection refused: {e}'}, status=500)
    
        if 'send_code' in request.POST:
            email_form = EmailForm(request.POST)
            if email_form.is_valid():
                email = email_form.cleaned_data['email']
                try:
                    user = User.objects.get(email=email)
                    code = str(random.randint(100000, 999999))
                    request.session['reset_code'] = code
                    request.session['reset_email'] = email

                    send_mail(
                        'Сброс пароля',
                        f'Ваш код для сброса пароля: {code}',
                        'noreply@somehost.local', 
                        ['nuraj9663@gmail.com'],
                        fail_silently=False,
                    )
                    redirect('reset_password')
                    messages.success(request, 'Код был отправлен на вашу почту.')
                except User.DoesNotExist:
                    messages.error(request, 'Пользователь с таким email не найден.')
            else:
                messages.error(request, 'Пожалуйста, введите корректный email.')

    return render(request, 'user/forgot_password.html', locals())


def reset_password(request):
    setting = Setting.objects.latest('id')
    cart_items = CartItem.objects.all()
    cart_items_count = cart_items.count()
    if request.method == 'POST':
        if 'email_send' in request.POST:
            email = request.POST.get('email')
            try:
                # Сохранение email в базе данных
                Subscribe.objects.create(email=email)
                
                # Отправка письма
                send_mail(
                    'Подписка на рассылку',  # Subject
                    f'Ваша почта: {email}\nСпасибо за подписку!',  # Message
                    'noreply@somehost.local',  # From email
                    [email],  # To email
                    fail_silently=False,
                )
                return redirect('reset_password')
            except BadHeaderError:
                return JsonResponse({'error': 'Invalid header found.'}, status=500)
            except ConnectionRefusedError as e:
                return JsonResponse({'error': f'Connection refused: {e}'}, status=500)
        if 'reset_password' in request.POST:  # Это означает, что была отправлена форма сброса пароля
            form = ResetPasswordForm(request.POST)
            if form.is_valid():
                code = form.cleaned_data['code']
                new_password = form.cleaned_data['new_password']
                confirm_password = form.cleaned_data['confirm_password']

                if code == request.session.get('reset_code'):
                    if new_password == confirm_password:
                        try:
                            email = request.session.get('reset_email')
                            user = User.objects.get(email=email)
                            user.set_password(new_password)
                            user.save()

                            # Автоматический вход пользователя
                            user = authenticate(request, username=user.username, new_password=new_password)
                            if user is not None:
                                login(request, user)
                                messages.success(request, 'Пароль успешно изменен.')
                                return redirect('index')  # Перенаправление на главную страницу
                            else:
                                messages.error(request, 'Не удалось войти. Попробуйте еще раз.')
                        except User.DoesNotExist:
                            messages.error(request, 'Произошла ошибка. Попробуйте еще раз.')
                    else:
                        messages.error(request, 'Пароли не совпадают.')
                else:
                    messages.error(request, 'Неверный код.')
            else:
                messages.error(request, 'Пожалуйста, заполните все поля.')

    return render(request, 'user/reset_password.html', locals())