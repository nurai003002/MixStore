# Generated by Django 5.0.6 on 2024-08-05 08:41

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('settings', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='setting',
            name='facebook',
        ),
    ]
