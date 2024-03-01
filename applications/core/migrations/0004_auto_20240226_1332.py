# Generated by Django 3.2 on 2024-02-26 07:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0003_auto_20240226_1149'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='fileshousing',
            options={'verbose_name': 'Файл жилья', 'verbose_name_plural': 'Файлы жилья'},
        ),
        migrations.AddField(
            model_name='vacancy',
            name='housing_status',
            field=models.BooleanField(default=False, verbose_name='Жилье предоставляется'),
        ),
    ]