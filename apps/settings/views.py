from django.shortcuts import render, redirect
from django.core.mail import send_mail, BadHeaderError
from django.http import JsonResponse

from apps.settings.models import Setting, Contacts
from apps.secondary.models import Slider, Service, Team, Review, Subscribe
from apps.products.models import Product, Category
from apps.cart.models import CartItem
from apps.telegram_bot.views import get_text
# Create your views here.

def index(request):
    setting = Setting.objects.latest('id')
    slider = Slider.objects.all()
    products = Product.objects.all()
    category = Category.objects.all().order_by('-id')[:3]
    categories = Category.objects.all()
    cart_items = CartItem.objects.all()  
    if request.user.is_authenticated:
        cart_items = CartItem.objects.filter(user=request.user)
    else:
        # Если пользователь не аутентифицирован, корзина привязывается к сессии
        session_key = request.session.session_key
        if not session_key:
            request.session.create()
        cart_items = CartItem.objects.filter(session_key=session_key)
    
    cart_items_count = cart_items.count()
    product_new = Product.objects.all().order_by('id')[:8]
    product_trand =  Product.objects.all()[:6]
    all_review = Review.objects.all()
    new_products_indices = [product.id for product in Product.objects.all().order_by('-id')[:3]]
    if request.method == "POST":
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
                return redirect('index')
            except BadHeaderError:
                return JsonResponse({'error': 'Invalid header found.'}, status=500)
            except ConnectionRefusedError as e:
                return JsonResponse({'error': f'Connection refused: {e}'}, status=500)
    return render(request, 'base/index.html', locals())


def contact(request):
    setting = Setting.objects.latest('id')
    slider = Slider.objects.all()
    service = Service.objects.latest('id')
    cart_items = CartItem.objects.all()  
    if request.user.is_authenticated:
        cart_items = CartItem.objects.filter(user=request.user)
    else:
        # Если пользователь не аутентифицирован, корзина привязывается к сессии
        session_key = request.session.session_key
        if not session_key:
            request.session.create()
        cart_items = CartItem.objects.filter(session_key=session_key)
    
    cart_items_count = cart_items.count()
    categories = Category.objects.all()
    team = Team.objects.all()
    if request.method=="POST":
        if 'contact_form' in request.POST:
            name = request.POST.get('name')
            email = request.POST.get('email')
            phone = request.POST.get('phone')
            message = request.POST.get('message')
            page_contact = Contacts.objects.create(name=name, email=email, phone=phone, message=message)
            if page_contact:
                get_text(f"""
                Оставлена заявка на обратный звонок 📞
                         
    Имя пользователя:  {name}
    Почта: {email}
    Номер телефона: {phone}
    Сообщение: {message}

    """)
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
     
    return render(request, 'base/contact.html', locals())