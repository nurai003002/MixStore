# Generated by Django 5.0.6 on 2024-08-05 09:36

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0004_category_link_alter_category_image'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='category',
            name='slug',
        ),
    ]
