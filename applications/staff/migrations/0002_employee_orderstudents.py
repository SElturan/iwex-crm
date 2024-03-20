# Generated by Django 4.2 on 2024-03-20 08:19

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('staff', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Employee',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(blank=True, max_length=50, verbose_name='Имя')),
                ('last_name', models.CharField(blank=True, max_length=50, verbose_name='Фамилия')),
                ('middle_name', models.CharField(blank=True, max_length=50, verbose_name='Отчество')),
                ('email', models.EmailField(blank=True, max_length=254, verbose_name='Контактный Email')),
                ('department', models.CharField(blank=True, max_length=255, verbose_name='Отдел')),
                ('position', models.CharField(blank=True, max_length=255, verbose_name='Должность')),
                ('birthday', models.DateField(blank=True, null=True, verbose_name='Дата рождения')),
                ('mobile_phone', models.CharField(blank=True, max_length=20, verbose_name='Мобильный телефон')),
                ('internal_phone', models.CharField(blank=True, max_length=20, verbose_name='Внутренний телефон')),
                ('is_created', models.BooleanField(default=True, verbose_name='Запись создана')),
                ('is_updated', models.BooleanField(default=False, verbose_name='Запись обновлена')),
                ('is_deleted', models.BooleanField(default=False, verbose_name='Запись удалена')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Пользователь')),
            ],
            options={
                'verbose_name': 'Сотрудник',
                'verbose_name_plural': 'Сотрудники',
            },
        ),
        migrations.CreateModel(
            name='OrderStudents',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('language_german_level', models.CharField(max_length=50, verbose_name='Уровень знания немецкого языка')),
                ('language_english_level', models.CharField(max_length=50, verbose_name='Уровень знания английского языка')),
                ('number_of_students', models.PositiveIntegerField(verbose_name='Количество студентов')),
                ('created_date', models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')),
                ('branch', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.branch', verbose_name='Филиал')),
                ('employer_sender', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='sent_orders', to='core.employercompany', verbose_name='Работодатель отправитель')),
                ('recipient_employee', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='received_orders', to='staff.employee', verbose_name='Сотрудник-получатель')),
            ],
            options={
                'verbose_name': 'Заказ студентов',
                'verbose_name_plural': 'Заказы студентов',
            },
        ),
    ]
