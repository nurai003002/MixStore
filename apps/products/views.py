from django.shortcuts import render, redirect
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import get_object_or_404

from apps.settings.models import Setting
from apps.products.models import Product, Category, ProductReview
from apps.cart.models import Cart
from apps.users.models import User

def product(request):
    setting = Setting.objects.latest('id')
    products = Product.objects.all().order_by('-id') 
    
    categories = Category.objects.all()
    cart_items = Cart.objects.all()
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

    return render(request, 'product/products.html', locals())

def product_detail(request, id):
    setting = Setting.objects.latest('id')
    products = Product.objects.all()
    random_products = Product.objects.all().order_by('?')[:5]
    categories = Category.objects.all()
    cart_items = Cart.objects.all()  
    cart_items_count = cart_items.count()
    product_detail = get_object_or_404(Product, id=id)
    reviews = ProductReview.objects.filter(product=product_detail).order_by('-created_at')
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
            
    return render(request, 'product/details.html', locals())


def product_list(request, category_id=None):
    categories = Category.objects.all()
    if category_id:
        products = Product.objects.filter(category_id=category_id).order_by('-id')
    else:
        products = Product.objects.all().order_by('-id')

    return render(request, 'product/products.html', locals())
