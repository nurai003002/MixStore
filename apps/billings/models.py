from django.db import models

class Billings(models.Model):
    first_name = models.CharField(
        max_length=255, verbose_name="Имя",
        blank=True, null=True
    )
    last_name = models.CharField(
        max_length=255, verbose_name="Фамилия",
        blank=True, null=True
    )
    city = models.CharField(
        max_length = 255,
        verbose_name = 'Город'
    )
    home = models.CharField(
        max_length = 255,
        verbose_name = 'Дом'
    )
    phone = models.CharField(
        max_length=255, verbose_name="Телефонный номер",
        blank=True, null=True
    )
    notes = models.TextField(
        verbose_name ='Примечание',
        blank=True, null=True
    )

    def __str__(self):
        return self.first_name  
    
    class Meta:
        verbose_name = 'Биллинг'
        verbose_name_plural = 'Биллинги'
