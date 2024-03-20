# Generated by Django 4.2 on 2024-03-19 04:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0003_alter_user_role'),
        ('core', '0004_auto_20240226_1332'),
    ]

    operations = [
        migrations.RemoveIndex(
            model_name='interviews',
            name='core_interv_user_id_9f9789_idx',
        ),
        migrations.RemoveField(
            model_name='vacancy',
            name='phone',
        ),
        migrations.RemoveField(
            model_name='interviews',
            name='user',
        ),
        migrations.AddField(
            model_name='interviews',
            name='user',
            field=models.ManyToManyField(to='accounts.profile', verbose_name='Профиль студента'),
        ),
    ]
