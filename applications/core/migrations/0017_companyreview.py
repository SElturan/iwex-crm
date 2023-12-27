# Generated by Django 3.2 on 2023-09-28 08:10

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('core', '0016_employercompany_description'),
    ]

    operations = [
        migrations.CreateModel(
            name='CompanyReview',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('rating', models.PositiveSmallIntegerField(choices=[(1, '1 Star'), (2, '2 Stars'), (3, '3 Stars'), (4, '4 Stars'), (5, '5 Stars')], verbose_name='Рейтинг')),
                ('comment', models.TextField(blank=True, verbose_name='Комментарий')),
                ('is_review_confirmed', models.BooleanField(default=False, verbose_name='Прошел модерацию')),
                ('created_date', models.DateTimeField(auto_now_add=True, verbose_name='Дата публикации')),
                ('company', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='reviews', to='core.employercompany')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Пользователь')),
            ],
            options={
                'verbose_name': 'Отзыв о компании',
                'verbose_name_plural': 'Отзывы о компаниях',
            },
        ),
    ]
