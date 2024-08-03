from django.shortcuts import render

from apps.settings.models import Setting, Contacts
from apps.secondary.models import Slider, Service, Team
from apps.products.models import Product, Category
from apps.cart.models import CartItem
from apps.telegram_bot.views import get_text
# Create your views here.

def index(request):
    setting = Setting.objects.latest('id')
    slider = Slider.objects.all()
    products = Product.objects.all()
    categories = Category.objects.all()
    cart_items = CartItem.objects.all()  
    cart_items_count = cart_items.count()
    product_trand =  Product.objects.all()[:6]
    return render(request, 'base/index.html', locals())


def contact(request):
    setting = Setting.objects.latest('id')
    slider = Slider.objects.all()
    service = Service.objects.latest('id')
    cart_items = CartItem.objects.all()  
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
     
    return render(request, 'base/contact.html', locals())