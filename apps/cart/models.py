from django.db import models
from django_resized.forms import ResizedImageField

from apps.products.models import Product
from apps.users.models import User
# Create your models here.
# class Cart(models.Model):
#     image = ResizedImageField(
#         force_format="WEBP", 
#         quality=100, 
#         upload_to='image/',
#         verbose_name="Фото изделий",
#         blank=True, null=True
#     )
#     COLOR_CHOICES = (
#         ('WHITE', 'WHITE'),
#         ('BLACK', 'BLACK'),
#         ('GRAY', 'GRAY'),
#         ('BROWN', 'BROWN'),
#     )
#     SIZE_CHOICES = (
#         ('XS', 'XS'),
#         ('S', 'S'),
#         ('M', 'M'),
#         ('L', 'L'),
#         ('XL', 'XL')
#     )
#     title = models.CharField(
#         max_length = 255,
#         verbose_name = "Название"
#     )
#     price = models.CharField(
#         max_length=255, 
#         verbose_name='Цена сейчас'
#     )
#     color = models.CharField(
#         max_length=255,
#         verbose_name='Цвета',
#         choices=COLOR_CHOICES,
#         blank=True, null=True
#     )
#     size = models.CharField(
#         max_length=100, verbose_name="Размер товара",
#         choices=SIZE_CHOICES,
#         default="S",
#         blank=True, null=True
#     )
#     quantity = models.PositiveIntegerField(
#         verbose_name = 'Количество продукта',
#         blank=True, null=True
#     )
#     total = models.PositiveBigIntegerField(
#         default=0, 
#         verbose_name="Итоговая цена товаров")
    
#     def __str__(self):
#         return self.title
    
#     class Meta:
#         verbose_name = 'Корзина'
#         verbose_name_plural = 'Корзина'


class CartItem(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE,blank=True, null=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE,blank=True, null=True)
    session_key = models.CharField(
        max_length=40,
        null=True, blank=True
    )
    image = ResizedImageField(
        force_format="WEBP", 
        quality=100, 
        upload_to='image/',
        verbose_name="Фото изделий",
        blank=True, null=True
    )
    title = models.CharField(
        max_length = 255,
        verbose_name = "Название"
    )
    price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name='Цена сейчас'
    )
    color = models.CharField(
        max_length=255,
        verbose_name='Цвета',
        blank=True, null=True
    )
    size = models.CharField(
        max_length=100, verbose_name="Размер товара",
        default="S",
        blank=True, null=True
    )
    quantity = models.IntegerField(
        verbose_name = 'Количество заказанного продукта',
        blank=True, null=True
    )
    total = models.DecimalField(
        max_digits=10, 
        decimal_places=2,
        verbose_name="Итоговая цена товаров"
    )

    def __str__(self):
        return f"{self.product.title} - {self.quantity} шт."
    
    class Meta:
        verbose_name = "Товар в корзине"
        verbose_name_plural = "Товары в корзине"
