from django.urls import path
from apps.products.views import product, product_detail,product_list, search

urlpatterns = [
    path('', product, name='product_index'),
    path('<int:id>/', product_detail, name='product_detail'),
    path('category/<int:category_id>/', product_list, name='product_list_by_category'),
    path('search/', search, name='search'),
]