from django.shortcuts import render,redirect,get_object_or_404
from apps.telegram_bot.views import get_text

from apps.settings.models import Setting, About
from apps.products.models import Product, Category
from apps.cart.models import Cart, CartItem
from apps.billings.models import Billings
# Create your views here.

def cart(request):
    setting = Setting.objects.latest('id')
    products = Product.objects.all()
    categories = Category.objects.all()
    cart_items = Cart.objects.all()
    cart_items_count = cart_items.count()
    
    return render(request, 'cart/cart.html', locals())

def add_to_cart(request, product_id):
    product_item = get_object_or_404(Product, pk=product_id)

    cart_item, created = Cart.objects.get_or_create(
        title=product_item.title,
        price=product_item.price,
        image=product_item.image,
        color=product_item.color,
        size=product_item.size,
    )
    return redirect('cart')


def remove_from_cart(request, cart_item_id):
    cart_item = get_object_or_404(Cart, pk=cart_item_id)
    cart_item.delete()
    return redirect('cart')


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
    return render(request, 'cart/checkout.html', locals())

