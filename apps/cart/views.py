from django.shortcuts import render,redirect,get_object_or_404

from apps.settings.models import Setting
from apps.products.models import Product, Category
from apps.cart.models import Cart, CartItem

# Create your views here.

def cart(request):
    setting = Setting.objects.latest('id')
    products = Product.objects.all()
    categories = Category.objects.all()
    cart_items = Cart.objects.all()
    cart_items_count = cart_items.count()
    total_price = sum([cart_item.total for cart_item in cart_items])
    for item in cart_items:
        item_price = item.price if item.price is not None else 0
        item_quantity = item.quantity if item.quantity is not None else 1
        item.total = item_price * item_quantity
    

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
    if request.method == 'POST':
        quantity = int(request.POST.get('quantity', 1))
        product = get_object_or_404(Product, id=id)
        
        # Предполагается, что у вас есть модель Cart с полем quantity
        cart_item, created = Cart.objects.get_or_create(product=product, user=request.user)
        if not created:
            cart_item.quantity += quantity
        else:
            cart_item.quantity = quantity
        cart_item.save()
        
        return redirect('cart')
    return redirect('cart')


def remove_from_cart(request, cart_item_id):
    cart_item = get_object_or_404(Cart, pk=cart_item_id)
    cart_item.delete()
    return redirect('cart')



def update_cart_item(request, product_id):
    if request.method == 'POST':
        cart_item = get_object_or_404(Cart, product_id=product_id, user=request.user)
        quantity = int(request.POST.get('quantity', 1))
        if quantity > 0:
            cart_item.quantity = quantity
            cart_item.save()
        else:
            cart_item.delete()
        
    return redirect('cart')