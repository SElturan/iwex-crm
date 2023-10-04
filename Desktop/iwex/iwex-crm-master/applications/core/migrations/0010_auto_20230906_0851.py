# Generated by Django 3.2 on 2023-09-06 08:51

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0005_alter_user_avatar'),
        ('core', '0009_vacancy_required_positions'),
    ]

    operations = [
        migrations.AddField(
            model_name='vacancy',
            name='required_positions_reviews',
            field=models.PositiveIntegerField(default=0, verbose_name='Колличество одобренных вакансии'),
        ),
        migrations.CreateModel(
            name='ReviewVacancy',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('check_profile', models.CharField(blank=True, choices=[('Approved', 'Одобрено'), ('Under_consideration', 'На расмотрении'), ('Rejected', 'Отказано')], default='Under_consideration', max_length=20, verbose_name='Статус отклика')),
                ('profile_review', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='accounts.profile', verbose_name='Профили на отклик')),
                ('vacancy_review', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.employercompany', verbose_name='Работадатель')),
            ],
            options={
                'verbose_name': 'Отклик на вакансию',
                'verbose_name_plural': 'Отклики на вакансии',
            },
        ),
    ]
