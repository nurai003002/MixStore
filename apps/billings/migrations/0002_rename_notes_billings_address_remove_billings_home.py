# Generated by Django 5.0.6 on 2024-08-06 10:40

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('billings', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='billings',
            old_name='notes',
            new_name='address',
        ),
        migrations.RemoveField(
            model_name='billings',
            name='home',
        ),
    ]
