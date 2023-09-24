from django.db import models
from django.urls import reverse
from users.models import User


class Diagnosis(models.Model):
    title = models.CharField(verbose_name='Название', max_length=200)
    description = models.TextField(verbose_name='Описание', max_length=500)
    date = models.DateTimeField(verbose_name='Дата постановки диагноза',
                                default=None, null=True)
    complaints = models.TextField(verbose_name='Жалобы', max_length=500)
    objective_status = models.TextField(verbose_name='Объективный статус',
                                        max_length=500)
    treatment = models.TextField(verbose_name='Лечение', max_length=500)
    prognosis = models.TextField(verbose_name='Прогноз', max_length=500)
    diagnosticstudies = models.ForeignKey(
        'DiagnosticStudies',
        verbose_name='Диагностические исследования',
        on_delete=models.CASCADE,
        related_query_name='diagnosis'
    )

    def __str__(self):
        return self.title


class DiagnosticStudies(models.Model):
    title = models.CharField(verbose_name='Название',
                             max_length=200)
    description = models.TextField(verbose_name='Описание', max_length=500)
    date = models.DateTimeField(verbose_name='Дата проведения манипуляции',
                                default=None, null=True)
    price = models.IntegerField(verbose_name='Стоимость', default=0)

    def __str__(self):
        return f'{self.title}'

    def get_absolute_url(self):
        return reverse('diagnostic_studies_detail', args=[self.pk])


class Doctor(models.Model):
    first_name = models.CharField(max_length=20, verbose_name='Имя')
    middle_name = models.CharField(max_length=20, verbose_name='Отчество')
    last_name = models.CharField(max_length=20, verbose_name='Фамилия')
    email = models.EmailField(verbose_name='Электронная почта', unique=True)
    specialization = models.CharField(verbose_name='Специализация',
                                      max_length=200)
    image = models.ImageField(verbose_name='Фотография', upload_to='images/',
                              default=None, null=True)
    patients = models.ManyToManyField(User, verbose_name='Пациенты',
                                      related_name='doctors',
                                      related_query_name='doctor')
    diagnostics = models.ManyToManyField(
        DiagnosticStudies,
        verbose_name='Диагностические манипуляции',
        related_name='doctors',
        related_query_name='doctor')
    diseases = models.ManyToManyField(Diagnosis, verbose_name='Заболевания',
                                      related_name='doctors',
                                      related_query_name='doctor', blank=True)

    @property
    def full_name(self):
        return f'{self.last_name} {self.first_name} {self.middle_name}'

    def __str__(self):
        return f'{self.full_name}, {self.specialization}'


class Appointment(models.Model):
    patient = models.ForeignKey(User, on_delete=models.CASCADE)
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE)
    date = models.DateTimeField()
    confirmed = models.BooleanField(default=False)

    class Meta:
        unique_together = ('patient', 'doctor', 'date')
