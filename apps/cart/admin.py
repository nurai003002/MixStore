from django.contrib import admin
from apps.cart.models import CartItem

# Register your models here.
# @admin.register(Cart)
# class CartAdmin(admin.ModelAdmin):
#     list_display = ('id', 'title', 'quantity')
#     inlines = (CartItemTabularInline, )

@admin.register(CartItem)
class CartItemAdmin(admin.ModelAdmin):
    list_display = ('id', 'quantity', )