# Generated by Django 3.2 on 2023-12-25 07:51

import ckeditor.fields
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('common', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Logo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(upload_to='logos/', verbose_name='Изображение логотипа')),
                ('description', models.TextField(blank=True, verbose_name='Описание логотипа')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='Дата последнего обновления')),
                ('external_url', models.URLField(blank=True, verbose_name='Внешний URL логотипа')),
                ('created_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Создано пользователем')),
            ],
            options={
                'verbose_name': 'Лого сайта',
                'verbose_name_plural': 'Лого сайтов',
            },
        ),
        migrations.CreateModel(
            name='FooterLink',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('instagram_link', models.CharField(blank=True, max_length=100, null=True, verbose_name='Ссылка на Instagram')),
                ('facebook_link', models.CharField(blank=True, max_length=100, null=True, verbose_name='Ссылка на Facebook')),
                ('whatsapp_link', models.CharField(blank=True, max_length=100, null=True, verbose_name='Ссылка на WhatsApp')),
                ('phone_number', models.CharField(blank=True, max_length=20, null=True, verbose_name='Номер телефона')),
                ('address', models.CharField(blank=True, max_length=200, null=True, verbose_name='Адрес')),
                ('email', models.EmailField(blank=True, max_length=254, null=True, verbose_name='Email')),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now, verbose_name='Дата создания')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='Дата обновления')),
                ('text', ckeditor.fields.RichTextField(verbose_name='Текст для футера')),
                ('created_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='created_footer_links', to=settings.AUTH_USER_MODEL, verbose_name='Создано пользователем')),
            ],
            options={
                'verbose_name': 'Информация внизу сайта',
                'verbose_name_plural': 'Информации внизу сайта',
            },
        ),
    ]