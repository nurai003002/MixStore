from django.shortcuts import render,redirect,get_object_or_404
from django.core.mail import send_mail, BadHeaderError
from django.http import JsonResponse

from apps.settings.models import Setting
from apps.products.models import Product, Category
from apps.cart.models import CartItem
from apps.secondary.models import Subscribe

# Create your views here.

def cart(request):
    setting = Setting.objects.latest('id')
    products = Product.objects.all()
    categories = Category.objects.all()
    cart_items = CartItem.objects.all()
    cart_items_count = cart_items.count()
    total_price = sum([cart_items.total for cart_items in cart_items])

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
                return redirect('cart')
            except BadHeaderError:
                return JsonResponse({'error': 'Invalid header found.'}, status=500)
            except ConnectionRefusedError as e:
                return JsonResponse({'error': f'Connection refused: {e}'}, status=500)
    

    return render(request, 'cart/cart.html', locals())

def add_to_cart(request, product_id):
    product_item = get_object_or_404(Product, pk=product_id)
    cart = request.session.get('cart', [])
    
    for item in cart:
        if item['product_id'] == product_id:
            item['quantity'] += 1
            item['total'] = item['price'] * item['quantity']
            break
    else:
        cart.append({
            'product_id': product_id,
            'quantity': 1,
            'title': product_item.title,
            'price': product_item.price,
            'image': str(product_item.image), 
            'color': product_item.color,
            'size': product_item.size,
            'total': product_item.price
        })
    
    # Обновляем сессию
    request.session['cart'] = cart
    request.session.modified = True

    # Синхронизация с базой данных
    if request.user.is_authenticated:
        user = request.user
    else:
        user = None

    cart_item, created = CartItem.objects.get_or_create(
        product=product_item,
        user=user,
        session_key=request.session.session_key,
        defaults={
            'quantity': 1,
            'price': product_item.price,
            'total': product_item.price,
            'image': product_item.image,
            'color': product_item.color,
            'size': product_item.size
        }
    )
    
    if not created:
        cart_item.quantity += 1
        cart_item.total = cart_item.price * cart_item.quantity
        cart_item.save()

    return redirect('cart')

def remove_from_cart(request, cart_item_id):
    cart_item = get_object_or_404(CartItem, pk=cart_item_id)
    cart_item.delete()
    return redirect('cart')


def update_cart_item(request, product_id):
    if request.method == 'POST':
        cart_item = get_object_or_404(CartItem, product_id=product_id, user=request.user)
        quantity = int(request.POST.get('quantity', 1))
        if quantity > 0:
            cart_item.quantity = quantity
            cart_item.save()
        else:
            cart_item.delete()
        
    return redirect('cart')