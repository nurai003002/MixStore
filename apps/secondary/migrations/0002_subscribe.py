# Generated by Django 5.0.6 on 2024-08-05 10:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('secondary', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Subscribe',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('email', models.CharField(blank=True, max_length=255, null=True, verbose_name='Почта для рассылки')),
            ],
            options={
                'verbose_name': 'Рассылка',
                'verbose_name_plural': 'Рассылка',
            },
        ),
    ]
