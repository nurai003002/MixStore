from django.urls import path
from apps.products.views import product, product_detail

urlpatterns = [
    path('', product, name='product_index'),
    path('<int:id>/', product_detail, name='product_detail'),
]