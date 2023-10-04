# Generated by Django 3.2 on 2023-09-26 09:07

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0021_auto_20230926_0826'),
    ]

    operations = [
        migrations.CreateModel(
            name='StudentDocumentsProfileProxy',
            fields=[
            ],
            options={
                'verbose_name': 'Документ Студента',
                'verbose_name_plural': 'Документы Студентов',
                'proxy': True,
                'indexes': [],
                'constraints': [],
            },
            bases=('accounts.profile',),
        ),
        migrations.DeleteModel(
            name='StudentDocument',
        ),
    ]
