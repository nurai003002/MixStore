# Generated by Django 5.0.6 on 2024-08-05 09:31

import django_resized.forms
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0003_category_description_category_image'),
    ]

    operations = [
        migrations.AddField(
            model_name='category',
            name='link',
            field=models.URLField(blank=True, null=True, verbose_name='Ссылка URL'),
        ),
        migrations.AlterField(
            model_name='category',
            name='image',
            field=django_resized.forms.ResizedImageField(blank=True, crop=None, default='no_image.jpg', force_format='WEBP', keep_meta=True, null=True, quality=100, scale=None, size=[1920, 1080], upload_to='category_images/', verbose_name='фото категории'),
        ),
    ]
