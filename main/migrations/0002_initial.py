# Generated by Django 4.2.4 on 2023-09-21 07:24

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("main", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="doctor",
            name="patients",
            field=models.ManyToManyField(
                related_name="doctors",
                related_query_name="doctor",
                to=settings.AUTH_USER_MODEL,
                verbose_name="Пациенты",
            ),
        ),
        migrations.AddField(
            model_name="diagnosis",
            name="diagnosticstudies",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_query_name="diagnosis",
                to="main.diagnosticstudies",
                verbose_name="Диагностические исследования",
            ),
        ),
        migrations.AddField(
            model_name="appointment",
            name="doctor",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE, to="main.doctor"
            ),
        ),
        migrations.AddField(
            model_name="appointment",
            name="patient",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL
            ),
        ),
        migrations.AlterUniqueTogether(
            name="appointment",
            unique_together={("patient", "doctor", "date")},
        ),
    ]
