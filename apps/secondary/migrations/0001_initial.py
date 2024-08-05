# Generated by Django 5.0.6 on 2024-08-05 07:40

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Review',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(upload_to='review/image', verbose_name='Фотография')),
                ('name', models.CharField(max_length=100, verbose_name='Имя')),
                ('position', models.CharField(max_length=255, verbose_name='Должность')),
                ('comment', models.TextField(verbose_name='Комментарий')),
            ],
            options={
                'verbose_name': 'Отзыв',
                'verbose_name_plural': 'Отзывы',
            },
        ),
        migrations.CreateModel(
            name='Service',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('delivery', models.CharField(max_length=255, verbose_name='Название (доставки)')),
                ('delivery_desc', models.CharField(max_length=500, verbose_name='Описание (доставки)')),
                ('money', models.CharField(max_length=255, verbose_name='Название (гарантия на возврат)')),
                ('money_desc', models.CharField(max_length=500, verbose_name='Описание (гарантия на возврат)')),
                ('support', models.CharField(max_length=255, verbose_name='Название (онлайн поддержка)')),
                ('support_desc', models.CharField(max_length=500, verbose_name='Описание (онлайн поддержка)')),
            ],
            options={
                'verbose_name': 'Сервис',
                'verbose_name_plural': 'Сервисы',
            },
        ),
        migrations.CreateModel(
            name='Slider',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(upload_to='slider_image/', verbose_name='Фотография')),
                ('main_title', models.CharField(max_length=255, verbose_name='Заголовок')),
                ('title', models.CharField(max_length=255, verbose_name='Название товара')),
                ('price', models.IntegerField(verbose_name='цена')),
            ],
            options={
                'verbose_name': 'Слайд',
                'verbose_name_plural': 'Слайдер',
            },
        ),
        migrations.CreateModel(
            name='Team',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(upload_to='team/image', verbose_name='Фотография')),
                ('name', models.CharField(max_length=100, verbose_name='Имя')),
                ('position', models.CharField(max_length=255, verbose_name='Должность')),
            ],
            options={
                'verbose_name': 'Команда',
                'verbose_name_plural': 'Команда',
            },
        ),
    ]
