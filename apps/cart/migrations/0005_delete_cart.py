# Generated by Django 5.0.6 on 2024-08-06 10:40

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cart', '0004_remove_cartitem_product_alter_cartitem_color_and_more'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Cart',
        ),
    ]
