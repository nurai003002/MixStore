from django.contrib import admin
from apps.cart.models import Cart, CartItem

# Register your models here.
class CartItemTabularInline(admin.TabularInline):
    model = CartItem
    extra = 0

@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'quantity')
    inlines = (CartItemTabularInline, )

@admin.register(CartItem)
class CartItemAdmin(admin.ModelAdmin):
    list_display = ('cart', 'product', 'quantity', )