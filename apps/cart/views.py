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
    delivery_cost = 250
    total_price = sum([cart_items.total for cart_items in cart_items])
    if total_price < 15000:
        total_price += delivery_cost  # Добавляем стоимость доставки, если сумма заказа меньше 1500 сом
    else:
        free_delivery = True

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
    
    # Получение количества из GET параметра
    quantity_to_add = int(request.GET.get('quantity', 1))  # Default to 1 if not specified

    print(f"Добавляем количество: {quantity_to_add} для продукта ID: {product_id}")

    # Поиск продукта в корзине
    item_found = False
    for item in cart:
        if item['product_id'] == product_id:
            item['quantity'] += quantity_to_add
            item['total'] = item['price'] * item['quantity']
            item_found = True
            print(f"Обновлено количество в сессии: {item['quantity']} для продукта ID: {product_id}")
            break

    # Если продукт не найден в корзине, добавляем его
    if not item_found:
        cart.append({
            'product_id': product_id,
            'quantity': quantity_to_add,
            'title': product_item.title,
            'price': product_item.price,
            'image': str(product_item.image), 
            'color': product_item.color,
            'size': product_item.size,
            'total': product_item.price * quantity_to_add
        })
        print(f"Продукт ID: {product_id} добавлен в корзину с количеством: {quantity_to_add}")

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
            'quantity': quantity_to_add,
            'price': product_item.price,
            'total': product_item.price * quantity_to_add,
            'image': product_item.image,
            'color': product_item.color,
            'size': product_item.size
        }
    )
    
    if not created:
        cart_item.quantity += quantity_to_add
        cart_item.total = cart_item.price * cart_item.quantity
        cart_item.save()
        print(f"Обновлено количество в базе данных: {cart_item.quantity} для продукта ID: {product_id}")

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