# Generated by Django 3.2 on 2024-02-19 09:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0006_alter_vacancy_type_of_housing'),
    ]

    operations = [
        migrations.AddField(
            model_name='vacancy',
            name='holiday_end_date',
            field=models.DateField(blank=True, null=True, verbose_name='Дата конца каникул'),
        ),
        migrations.AddField(
            model_name='vacancy',
            name='holiday_start_date',
            field=models.DateField(blank=True, null=True, verbose_name='Дата начала каникул'),
        ),
    ]