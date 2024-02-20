# Generated by Django 3.2 on 2024-02-19 08:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0003_auto_20240216_1738'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='vacation_end_date',
            field=models.DateField(blank=True, null=True, verbose_name='Дата конца каникул'),
        ),
        migrations.AddField(
            model_name='profile',
            name='vacation_start_date',
            field=models.DateField(blank=True, null=True, verbose_name='Дата начала каникул'),
        ),
    ]
