from django.db import models
from apps.products.models import Product

class Billings(models.Model):
    first_name = models.CharField(
        max_length=255, verbose_name="Имя",
        blank=True, null=True
    )
    last_name = models.CharField(
        max_length=255, verbose_name="Фамилия",
        blank=True, null=True
    )
    phone = models.CharField(
        max_length=255, verbose_name="Телефонный номер",
        blank=True, null=True
    )
    address = models.TextField(
        verbose_name ='Примечание',
        blank=True, null=True
    )
    city = models.CharField(
        max_length = 255,
        verbose_name = 'Город'
    )

    def __str__(self):
        return self.first_name  
    
    class Meta:
        verbose_name = 'Биллинг'
        verbose_name_plural = 'Биллинги'
    
class BillingProduct(models.Model):
    billing = models.ForeignKey(
        Billings, on_delete=models.CASCADE, 
        related_name='billing_products', verbose_name="Биллинг"
    )
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, 
        related_name='products_billings', verbose_name="Товар"
    )
    quantity = models.PositiveIntegerField(
        verbose_name="Количество товаров"
    )
    price = models.PositiveBigIntegerField(
        verbose_name="Итоговая цена товара", default=0
    )
    status = models.BooleanField(
        verbose_name="Статус", default=False
    )
    created = models.DateTimeField(
        auto_now_add=True, verbose_name="Дата создания"
    )

    def __str__(self):
        return f"{self.billing} - {self.product} ({self.quantity} шт.)"
    
    class Meta:
        verbose_name = "Биллинг товара"
        verbose_name_plural = "Биллинги товаров"