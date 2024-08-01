from django.db import models
from django_resized.forms import ResizedImageField
# from ckeditor.fields import RichTextField
from django.contrib.auth import get_user_model

User = get_user_model()


# Create your models here.
class Setting(models.Model):
    title = models.CharField(
        max_length=100,
        verbose_name="Название сайта"
    )
    description = models.TextField(
        max_length=400,
        verbose_name="Описание",
        blank=True, null=True
    )
    logo = models.ImageField(
        upload_to='logo/',
        verbose_name="Логотип",
        blank=True, null=True
    )
    email = models.EmailField(
        verbose_name="Почта",
        blank=True, null=True
    )
    phone = models.CharField(
        max_length=100,
        verbose_name="Номер телефона",
        blank=True, null=True
    )
    schedule = models.CharField(
        max_length = 250,
        verbose_name = 'График работы',
        blank=True, null=True
    )
    address = models.CharField(
        max_length=300, 
        verbose_name="Адрес",
        blank=True, null=True
    )
    facebook = models.URLField(
        verbose_name="Facebook",
        blank=True, null=True
    )
    instagram = models.URLField(
        verbose_name="Instagram",
        blank=True, null=True
    )
    whatsapp = models.URLField(
        verbose_name="WhatsApp",
        blank=True,
        null=True
    )
    def __str__(self):
        return self.title 
    
    class Meta:
        verbose_name = "Настройка"
        verbose_name_plural = "Настройки"

class About(models.Model):
    banner = models.ImageField(
        upload_to='banner',
        verbose_name='Баннер о нас'
    )
    title = models.CharField(
        max_length=255,
        verbose_name='Название'
    )
    description = models.CharField(
        max_length=500,
        verbose_name='Описание'
    )

    def __str__(self):
        return self.title
    
    class Meta:
        verbose_name = 'О нас'
        verbose_name_plural = 'О нас'


class Contacts(models.Model):
    name = models.CharField(
        max_length = 255,
        verbose_name = 'Имя'
    )
    email = models.EmailField(
        verbose_name = "Почта"
    )
    phone = models.CharField(
        max_length = 255,
        verbose_name = 'Тема'
    )
    message = models.TextField(
        verbose_name = 'Сообщение'
    )

    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = 'Обратная связь'
        verbose_name_plural = 'Обратная связь'
