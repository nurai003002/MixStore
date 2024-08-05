from django.contrib import admin
from apps.products.models import Product, Category, ProductImage, ProductFeature, ProductReview
# Register your models here.

class ImageTabularInline(admin.TabularInline):
    model = ProductImage
    extra = 1

class FeatureTabularInline(admin.TabularInline):
    model = ProductFeature
    extra = 2

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'description')
    list_filter = ('id', 'title')
    inlines = (ImageTabularInline, FeatureTabularInline)

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'title')
    list_filter = ('id', 'title')

@admin.register(ProductReview)
class StarsProductAdmin(admin.ModelAdmin):
    list_display = ('user', 'text')
    search_fields = ('user__username', 'product__title')
