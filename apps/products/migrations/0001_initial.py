# Generated by Django 5.0.6 on 2024-08-05 07:40

import ckeditor.fields
import django.db.models.deletion
import django_resized.forms
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255, verbose_name='Название')),
                ('slug', models.SlugField(blank=True, max_length=100, unique=True, verbose_name='URL')),
            ],
            options={
                'verbose_name': 'Категория',
                'verbose_name_plural': 'Категории',
            },
        ),
        migrations.CreateModel(
            name='ProductFeature',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('feature', models.CharField(max_length=255, verbose_name='Характиристика товары')),
            ],
            options={
                'verbose_name': 'Характиристика торава',
                'verbose_name_plural': 'Характиристики товаров',
            },
        ),
        migrations.CreateModel(
            name='ProductImage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', django_resized.forms.ResizedImageField(crop=None, default='no_image.jpg', force_format='WEBP', keep_meta=True, quality=100, scale=None, size=[1920, 1080], upload_to='product_images/', verbose_name='Основная фотография')),
            ],
            options={
                'verbose_name': 'Фотография торава',
                'verbose_name_plural': 'Фотографии товаров',
            },
        ),
        migrations.CreateModel(
            name='ProductReview',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('email', models.EmailField(blank=True, max_length=254, null=True, verbose_name='Почта')),
                ('text', models.TextField(verbose_name='Текст для отзыва')),
                ('created_at', models.DateField(auto_now_add=True, verbose_name='Дата создания')),
            ],
            options={
                'verbose_name': 'Отзыв товара',
                'verbose_name_plural': 'Отзывы товаров',
            },
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255, verbose_name='Заголовок')),
                ('status', models.CharField(blank=True, choices=[('в наличии', 'В наличии'), ('нет в наличии', 'нет в наличии')], max_length=255, null=True, verbose_name='Статус')),
                ('description', ckeditor.fields.RichTextField(blank=True, null=True, verbose_name='Описание')),
                ('color', models.CharField(blank=True, max_length=255, null=True, verbose_name='Цвета')),
                ('size', models.CharField(blank=True, default='S', max_length=255, null=True, verbose_name='Размер товара')),
                ('image', django_resized.forms.ResizedImageField(blank=True, crop=None, default='no_image.jpg', force_format='WEBP', keep_meta=True, null=True, quality=100, scale=None, size=[1920, 1080], upload_to='product_images/', verbose_name='Основная фотография')),
                ('price', models.PositiveIntegerField(verbose_name='Цена')),
                ('old_price', models.PositiveIntegerField(blank=True, null=True, verbose_name='Старая цена')),
                ('category', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='category_products', to='products.category', verbose_name='Категория товара')),
            ],
            options={
                'verbose_name': 'Товар',
                'verbose_name_plural': 'Товары',
            },
        ),
    ]
