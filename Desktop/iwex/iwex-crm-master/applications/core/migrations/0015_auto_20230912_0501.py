# Generated by Django 3.2 on 2023-09-12 05:01

from django.db import migrations, models
from datetime import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0014_auto_20230911_0819'),
    ]

    operations = [
        migrations.AddField(
            model_name='vacancy',
            name='created_date',
            field=models.DateTimeField(auto_now_add=True, default=datetime(2022,5,20, 0, 0), verbose_name='Дата публикации'),
            preserve_default=False,
        ),
        migrations.DeleteModel(
            name='FavoriteVacancy',
        ),
    ]
