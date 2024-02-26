# Generated by Django 3.2 on 2024-02-16 09:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0003_auto_20240216_1501'),
    ]

    operations = [
        migrations.RemoveIndex(
            model_name='branch',
            name='core_branch_city_e9f930_idx',
        ),
        migrations.AddIndex(
            model_name='branch',
            index=models.Index(fields=['country'], name='core_branch_country_1c1e4f_idx'),
        ),
    ]