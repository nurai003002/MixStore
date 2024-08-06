# Generated by Django 5.0.6 on 2024-08-06 08:07

import django_resized.forms
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cart', '0002_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='cartitem',
            name='cart',
        ),
        migrations.AddField(
            model_name='cartitem',
            name='color',
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name='Цвет'),
        ),
        migrations.AddField(
            model_name='cartitem',
            name='image',
            field=django_resized.forms.ResizedImageField(crop=None, default='no_image.jpg', force_format='WEBP', keep_meta=True, quality=100, scale=None, size=[1920, 1080], upload_to='cart_images/', verbose_name='Фото'),
        ),
        migrations.AddField(
            model_name='cartitem',
            name='price',
            field=models.PositiveIntegerField(default=1, verbose_name='Цена'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='cartitem',
            name='size',
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name='Размер'),
        ),
        migrations.AddField(
            model_name='cartitem',
            name='title',
            field=models.CharField(default=1, max_length=255, verbose_name='Название'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='cartitem',
            name='quantity',
            field=models.PositiveIntegerField(default=1, verbose_name='Кол-во'),
        ),
        migrations.AlterField(
            model_name='cartitem',
            name='total',
            field=models.PositiveIntegerField(verbose_name='Общая сумма'),
        ),
    ]
