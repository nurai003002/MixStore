from django.shortcuts import render
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from apps.settings.models import Setting
from apps.products.models import Product, Category
from apps.cart.models import Cart


def product(request):
    setting = Setting.objects.latest('id')
    products = Product.objects.all()
    categories = Category.objects.all()
    cart_items = Cart.objects.all()  
    cart_items_count = cart_items.count()
    paginator = Paginator(products, 8)  

    color_query = request.GET.get('color')
    if color_query:
        products_list = products.filter(color=color_query.upper())     
    page = request.GET.get('page')
    try:
        products = paginator.page(page)
    except PageNotAnInteger:
        products = paginator.page(1)
    except EmptyPage:
        products = paginator.page(paginator.num_pages)
    return render(request, 'product/products.html', locals())

def product_detail(request, id):
    setting = Setting.objects.latest('id')
    products = Product.objects.all()
    categories = Category.objects.all()
    cart_items = Cart.objects.all()  
    cart_items_count = cart_items.count()
    product_detail = Product.objects.get(id=id)
    return render(request, 'product/details.html', locals())