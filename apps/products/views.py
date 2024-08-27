from django.shortcuts import render, redirect
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import get_object_or_404
from django.core.mail import send_mail, BadHeaderError
from django.http import JsonResponse
from django.urls import reverse
from django.db.models import Sum, Q, Count

from apps.settings.models import Setting
from apps.products.models import Product, Category, ProductReview
from apps.cart.models import CartItem
from apps.users.models import User
from apps.secondary.models import Subscribe

def product(request):
    setting = Setting.objects.latest('id')
    products = Product.objects.all().order_by('-id') 
    
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
    paginator = Paginator(products, 12)  

    color_query = request.GET.get('color')
    if color_query:
        products = products.filter(color=color_query.upper())

    page = request.GET.get('page')
    try:
        products = paginator.page(page)
    except PageNotAnInteger:
        products = paginator.page(1)
    except EmptyPage:
        products = paginator.page(paginator.num_pages)

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
                return redirect('product_index')
            except BadHeaderError:
                return JsonResponse({'error': 'Invalid header found.'}, status=500)
            except ConnectionRefusedError as e:
                return JsonResponse({'error': f'Connection refused: {e}'}, status=500)
    return render(request, 'product/products.html', locals())

def product_detail(request, id):
    setting = Setting.objects.latest('id')
    products = Product.objects.all()
    random_products = Product.objects.all().order_by('?')[:5]
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
    product_detail = get_object_or_404(Product, id=id)
    reviews = ProductReview.objects.filter(product=id).order_by('-created_at')
    new_products_indices = [product.id for product in Product.objects.all().order_by('-id')[:3]]
    reviews_count = reviews.count()

    if request.method == 'POST' and request.user.is_authenticated:
        if 'submit' in request.POST:
            text = request.POST.get('text')
            email = request.POST.get('email')
            if text and email:  # Проверка, что текст отзыва и email не пустые
                new_comment = ProductReview.objects.create(
                    product=product_detail, 
                    text=text, 
                    email=email, 
                    user=request.user
                )
                new_comment.save()
                return redirect('product_detail', id=id)
            
        if 'email_send' in request.POST:
            email = request.POST.get('email')
            try:
                Subscribe.objects.create(email=email)
                
                send_mail(
                    'Подписка на рассылку',  
                    f'Ваша почта: {email}\nСпасибо за подписку!',
                    'noreply@somehost.local', 
                    [email], 
                    fail_silently=False,
                )
                return redirect('product_detail', id=id)
            except BadHeaderError:
                return JsonResponse({'error': 'Invalid header found.'}, status=500)
            except ConnectionRefusedError as e:
                return JsonResponse({'error': f'Connection refused: {e}'}, status=500)
    return render(request, 'product/details.html', locals())


def product_list(request, category_id=None):
    categories = Category.objects.all()
    if category_id:
        products = Product.objects.filter(category_id=category_id).order_by('-id')
    else:
        products = Product.objects.all().order_by('-id')

    return render(request, 'product/products.html', locals())

def search(request):
    query = request.GET.get('query', '').strip()
    results = []
    
    if query:
        q_objects = Q()  # Создаем пустой Q-объект для накопления условий поиска
        
        # Поиск по первой букве
        q_objects |= Q(title__istartswith=query[0]) | Q(description__istartswith=query[0])
        
        # Поиск по первым трём буквам
        if len(query) >= 3:
            q_objects |= Q(title__istartswith=query[:3]) | Q(description__istartswith=query[:3])
        
        # Поиск по всему слову
        q_objects |= Q(title__icontains=query) | Q(description__icontains=query)
        
        products = Product.objects.filter(q_objects)
        
        # Формируем список результатов
        for product in products:
            product_url = reverse('product_detail', args=[product.id])
            results.append({
                'title': product.title,
                'price': product.price,
                'url': product_url
            })

        return JsonResponse({'results': results})
    return render(request, 'product/products.html', locals())
