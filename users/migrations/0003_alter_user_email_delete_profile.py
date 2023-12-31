# Generated by Django 4.2.4 on 2023-09-21 07:32

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("users", "0002_profile"),
    ]

    operations = [
        migrations.AlterField(
            model_name="user",
            name="email",
            field=models.EmailField(
                max_length=254,
                unique=True,
                validators=[
                    django.core.validators.EmailValidator(
                        message="Введите корректный адрес электронной почты"
                    )
                ],
                verbose_name="Электронная почта",
            ),
        ),
        migrations.DeleteModel(
            name="Profile",
        ),
    ]
