# Generated by Django 5.0.6 on 2024-08-06 12:00

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('billings', '0003_order_orderitem'),
        ('products', '0005_remove_category_slug'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='orderitem',
            name='order',
        ),
        migrations.RemoveField(
            model_name='orderitem',
            name='product',
        ),
        migrations.CreateModel(
            name='BillingProduct',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.PositiveIntegerField(verbose_name='Количество товаров')),
                ('price', models.PositiveBigIntegerField(default=0, verbose_name='Итоговая цена товара')),
                ('status', models.BooleanField(default=False, verbose_name='Статус')),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')),
                ('billing', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='billing_products', to='billings.billings', verbose_name='Биллинг')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='products_billings', to='products.product', verbose_name='Товар')),
            ],
            options={
                'verbose_name': 'Биллинг товара',
                'verbose_name_plural': 'Биллинги товаров',
            },
        ),
        migrations.DeleteModel(
            name='Order',
        ),
        migrations.DeleteModel(
            name='OrderItem',
        ),
    ]
