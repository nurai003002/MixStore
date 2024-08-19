from django.db import models
from django.contrib.auth import get_user_model
from ckeditor.fields import RichTextField
from django_resized.forms import ResizedImageField
# Create your models here.

class Category(models.Model):
    image = ResizedImageField(
        force_format="WEBP", 
        quality=100, default='no_image.jpg',
        upload_to='category_images/',
        verbose_name="фото категории",
        blank = True, null = True
    )
    description = models.CharField(
        max_length=500,
        verbose_name='Описание'
    )
    title = models.CharField(
        max_length=255, verbose_name="Название"
    )
    link = models.URLField(
        verbose_name='Ссылка URL',
        blank=True, null=True
    )
    
    def __str__(self):
        return self.title
    
    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "Категории"



User = get_user_model()

# Create your models here.
class Product(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.SET_NULL,
        related_name="user_products",
        verbose_name="Пользователь",
        blank=True, null=True
    )
    category = models.ForeignKey(
        Category, related_name="category_products",
        on_delete=models.SET_NULL,
        verbose_name="Категория товара",
        blank=True, null=True
    ) 
    STATUS_CHOICES = (
        ('в наличии', 'В наличии'),
        ('нет в наличии', 'нет в наличии'),
    )
    title = models.CharField(
        max_length=255,
        verbose_name="Заголовок"
    )
    status = models.CharField(
        max_length=255,
        choices=STATUS_CHOICES,
        verbose_name='Статус',
        blank=True, null=True
    )
    description = RichTextField(
        verbose_name="Описание",
        blank=True, null=True
    )
    color = models.CharField(
        max_length=255,
        verbose_name='Цвета',
        blank=True, null=True
    )
    size = models.CharField(
        max_length=255, verbose_name="Размер товара",
        default="S",
        blank=True, null=True
    )
    image = ResizedImageField(
        force_format="WEBP", 
        quality=100, default='no_image.jpg',
        upload_to='product_images/',
        verbose_name="Основная фотография",
        blank = True, null = True
    )
    price = models.IntegerField(
        verbose_name="Цена"
    )
    old_price = models.PositiveIntegerField(
        verbose_name="Старая цена",
        blank=True, null=True
    )
    quantity = models.IntegerField(
        verbose_name = 'Количество продукта',
        blank=True, null=True
    )
    def __str__(self):
        return f"{self.title} {self.price} KGS"

    class Meta:
        verbose_name = "Товар"
        verbose_name_plural = "Товары"


class ProductImage(models.Model):
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE,
        related_name="product_image",
        verbose_name="Товар"
    )
    image = ResizedImageField(
        force_format="WEBP", 
        quality=100, default='no_image.jpg',
        upload_to='product_images/',
        verbose_name="Основная фотография",
    )

    def __str__(self):
        return f"{self.product}"
    
    class Meta:
        verbose_name = "Фотография торава"
        verbose_name_plural = "Фотографии товаров"


class ProductFeature(models.Model):
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE,
        related_name="product_feature",
        verbose_name="Товар"
    )
    feature = models.CharField(
        max_length=255,
        verbose_name="Характиристика товары",
    )

    def __str__(self):
        return f"{self.product} - {self.feature}"
    
    class Meta:
        verbose_name = "Характиристика торава"
        verbose_name_plural = "Характиристики товаров"

class ProductReview(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE,
        related_name="user_reviews",
        verbose_name="Пользователь"
    )
    email = models.EmailField(
        verbose_name = 'Почта',
        blank=True, null=True,
    )
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE,
        related_name='reviews',
        verbose_name="Название товара"
    )
    text = models.TextField(
        verbose_name="Текст для отзыва"
    )
    created_at = models.DateField(
        auto_now_add=True,
        verbose_name='Дата создания'
    )

    def __str__(self):
        return f"Отзыв с {self.user.username} для {self.product.title}"

    class Meta:
        verbose_name = "Отзыв товара"
        verbose_name_plural = "Отзывы товаров"