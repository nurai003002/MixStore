# Generated by Django 5.0.6 on 2024-08-19 13:34

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cart', '0007_alter_cartitem_color_alter_cartitem_quantity_and_more'),
        ('products', '0009_remove_product_created'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name='cartitem',
            name='product',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='products.product'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='cartitem',
            name='session_key',
            field=models.CharField(blank=True, max_length=40, null=True),
        ),
        migrations.AddField(
            model_name='cartitem',
            name='user',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='cartitem',
            name='price',
            field=models.DecimalField(decimal_places=2, max_digits=10, verbose_name='Цена сейчас'),
        ),
        migrations.AlterField(
            model_name='cartitem',
            name='total',
            field=models.DecimalField(decimal_places=2, max_digits=10, verbose_name='Итоговая цена товаров'),
        ),
    ]
