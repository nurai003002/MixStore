# Generated by Django 5.0.6 on 2024-08-07 13:06

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('billings', '0007_alter_billingproduct_billing'),
    ]

    operations = [
        migrations.AlterField(
            model_name='billingproduct',
            name='billing',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='billing_products', to='billings.billings', verbose_name='Биллинг'),
        ),
    ]
