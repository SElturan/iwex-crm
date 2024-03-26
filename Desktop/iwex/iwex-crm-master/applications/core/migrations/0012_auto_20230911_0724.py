# Generated by Django 3.2 on 2023-09-11 07:24

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0006_alter_profile_user'),
        ('core', '0011_alter_reviewvacancy_vacancy_review'),
    ]

    operations = [
        migrations.RenameField(
            model_name='reviewvacancy',
            old_name='vacancy_review',
            new_name='vacancy',
        ),
        migrations.RemoveField(
            model_name='reviewvacancy',
            name='check_profile',
        ),
        migrations.RemoveField(
            model_name='reviewvacancy',
            name='profile_review',
        ),
        migrations.AddField(
            model_name='reviewvacancy',
            name='applicant_profile',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='accounts.profile', verbose_name='Профиль соискателя'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='reviewvacancy',
            name='employer',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='core.employercompany', verbose_name='Работодатель'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='reviewvacancy',
            name='employer_comment',
            field=models.TextField(blank=True, default='', verbose_name='Комментарий работодателя'),
        ),
        migrations.AddField(
            model_name='reviewvacancy',
            name='rejection_message',
            field=models.TextField(blank=True, default='', verbose_name='Сообщение об отказе'),
        ),
        migrations.AddField(
            model_name='reviewvacancy',
            name='status',
            field=models.CharField(choices=[('Approved', 'Одобрено'), ('Under_consideration', 'На рассмотрении'), ('Rejected', 'Отказано')], default='Under_consideration', max_length=20, verbose_name='Статус отклика'),
        ),
    ]
