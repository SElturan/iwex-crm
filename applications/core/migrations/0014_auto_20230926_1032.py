# Generated by Django 3.2 on 2023-09-26 10:32

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('core', '0013_vacancy_exchange'),
    ]

    operations = [
        migrations.AlterField(
            model_name='vacancy',
            name='exchange',
            field=models.CharField(blank=True, choices=[('RUB', 'RUB'), ('USD', 'USD'), ('EUR', 'EUR'), ('KGS', 'KGS'), ('KZT', 'KZT')], default='', max_length=10),
        ),
        migrations.CreateModel(
            name='Invitation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('message', models.TextField(blank=True)),
                ('status', models.CharField(choices=[('pending', 'Ожидает ответа'), ('accepted', 'Принято'), ('declined', 'Отклонено')], default='pending', max_length=10)),
                ('employer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.employercompany')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='invitations', to=settings.AUTH_USER_MODEL)),
                ('vacancy', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.vacancy')),
            ],
        ),
    ]
