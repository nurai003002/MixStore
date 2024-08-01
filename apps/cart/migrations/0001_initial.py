# Generated by Django 5.0.6 on 2024-07-31 09:46

import django.db.models.deletion
import django_resized.forms
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Cart',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', django_resized.forms.ResizedImageField(blank=True, crop=None, force_format='WEBP', keep_meta=True, null=True, quality=100, scale=None, size=[1920, 1080], upload_to='image/', verbose_name='Фото изделий')),
                ('title', models.CharField(max_length=255, verbose_name='Название')),
                ('price', models.CharField(max_length=255, verbose_name='Цена сейчас')),
                ('color', models.CharField(blank=True, choices=[('WHITE', 'WHITE'), ('BLACK', 'BLACK'), ('GRAY', 'GRAY'), ('BROWN', 'BROWN')], max_length=255, null=True, verbose_name='Цвета')),
                ('size', models.CharField(blank=True, choices=[('XS', 'XS'), ('S', 'S'), ('M', 'M'), ('L', 'L'), ('XL', 'XL')], default='S', max_length=100, null=True, verbose_name='Размер товара')),
                ('quantity', models.PositiveIntegerField(blank=True, null=True, verbose_name='Количество продукта')),
                ('total', models.PositiveBigIntegerField(default=0, verbose_name='Итоговая цена товаров')),
            ],
            options={
                'verbose_name': 'Корзина',
                'verbose_name_plural': 'Корзина',
            },
        ),
        migrations.CreateModel(
            name='CartItem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.PositiveIntegerField(default=1, verbose_name='Количество товара')),
                ('total', models.PositiveBigIntegerField(default=0, verbose_name='Итоговая цена товаров')),
                ('cart', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='cart.cart', verbose_name='Корзина')),
            ],
            options={
                'verbose_name': 'Товар в корзине',
                'verbose_name_plural': 'Товары в корзине',
            },
        ),
    ]
