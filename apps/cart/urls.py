from django.urls import path
from apps.cart.views import cart, add_to_cart, remove_from_cart, update_cart_quantity

urlpatterns = [
    path('',  cart, name='cart'),
    path('add_to_cart/<int:product_id>/', add_to_cart, name='add_to_cart'),
    path('remove_from_cart/<int:cart_item_id>/', remove_from_cart, name='remove_from_cart'),
    path('update-cart-item/<int:product_id>/', update_cart_quantity, name='update_cart_quantity')
]
