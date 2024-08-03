from django.db import models

# Create your models here.
class Slider(models.Model):
    image = models.ImageField(
        upload_to='slider_image/',
        verbose_name='Фотография'
    )
    main_title = models.CharField(
        max_length = 255,
        verbose_name = 'Заголовок'
    ) 
    title = models.CharField(
        max_length = 255,
        verbose_name = 'Название товара'
    ) 
    price = models.IntegerField(
        verbose_name = 'цена'
    )
    

    def __str__(self):
        return self.title
    
    class Meta:
        verbose_name = 'Слайд'
        verbose_name_plural = 'Слайдер'
        
class Service(models.Model):
    delivery = models.CharField(
        max_length = 255,
        verbose_name='Название (доставки)'
    )
    delivery_desc = models.CharField(
        max_length=500,
        verbose_name='Описание (доставки)'
    )
    money = models.CharField(
        max_length = 255,
        verbose_name='Название (гарантия на возврат)'
    )
    money_desc = models.CharField(
        max_length=500,
        verbose_name='Описание (гарантия на возврат)'
    )
    support = models.CharField(
        max_length = 255,
        verbose_name='Название (онлайн поддержка)'
    )
    support_desc = models.CharField(
        max_length=500,
        verbose_name='Описание (онлайн поддержка)'
    )

    def __str__(self):
        return self.delivery
    
    class Meta:
        verbose_name = 'Сервис'
        verbose_name_plural = 'Сервисы'

class Team(models.Model):
    image = models.ImageField(
        upload_to='team/image',
        verbose_name='Фотография'
    )
    name = models.CharField(
        max_length=100,
        verbose_name='Имя'
    )
    position = models.CharField(
        max_length=255,
        verbose_name='Должность'
    )

    def __str__(self):
        return f"{self.name} - {self.position}"
    
    class Meta:
        verbose_name = 'Команда'
        verbose_name_plural = 'Команда'
        
class Review(models.Model):
    image = models.ImageField(
        upload_to='review/image',
        verbose_name='Фотография'
    )
    name = models.CharField(
        max_length=100,
        verbose_name='Имя'
    ) 
    position = models.CharField(
        max_length=255,
        verbose_name='Должность'
    )
    comment = models.TextField(
        verbose_name = 'Комментарий'
    )

    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'