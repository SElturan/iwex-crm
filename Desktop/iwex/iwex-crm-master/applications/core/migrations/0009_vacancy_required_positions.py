# Generated by Django 3.2 on 2023-09-06 05:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0008_auto_20230905_0440'),
    ]

    operations = [
        migrations.AddField(
            model_name='vacancy',
            name='required_positions',
            field=models.PositiveIntegerField(default=1, verbose_name='Требуемое количество мест'),
        ),
    ]