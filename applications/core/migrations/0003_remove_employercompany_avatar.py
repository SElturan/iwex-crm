# Generated by Django 3.2 on 2023-08-30 09:05

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0002_auto_20230830_0502'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='employercompany',
            name='avatar',
        ),
    ]
