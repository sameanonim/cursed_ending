from django.contrib.auth.models import AbstractUser
from django.db import models
from django.urls import reverse
from django.template.defaultfilters import slugify

from users.validators import (BLOOD_GROUP_CHOICES, GENDER_CHOICES,
                              email_validator, phone_validator,
                              image_validator)

NULLABLE = {'blank': True, 'null': True}


class User(AbstractUser):
    """Модель пользователя"""
    first_name = models.CharField(max_length=20, verbose_name='Имя')
    middle_name = models.CharField(max_length=20, verbose_name='Отчество')
    last_name = models.CharField(max_length=20, verbose_name='Фамилия')
    slug = models.SlugField(verbose_name='URL', max_length=255, blank=True,
                            unique=True)
    photo = models.ImageField(
        upload_to='users/',
        verbose_name='Фотография',
        validators=[image_validator],
        **NULLABLE)
    birth_date = models.DateField(verbose_name='Дата рождения', **NULLABLE)
    email = models.EmailField(max_length=254, verbose_name='Электронная почта',
                              validators=[email_validator], unique=True)
    insurance_policy = models.CharField(max_length=20,
                                        verbose_name='Страховой полис',
                                        unique=True)
    gender = models.CharField(max_length=20, verbose_name='Пол',
                              choices=GENDER_CHOICES)
    phone = models.CharField(max_length=20, verbose_name='Телефон',
                             validators=[phone_validator],
                             **NULLABLE)
    blood_group = models.CharField(max_length=20, verbose_name='Группа крови',
                                   choices=BLOOD_GROUP_CHOICES)
    city = models.CharField(max_length=20, verbose_name='Город',
                            **NULLABLE)
    is_active = models.BooleanField(default=True, verbose_name='активный',
                                    **NULLABLE)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    def __str__(self):
        return f"{self.last_name} {self.first_name} {self.middle_name}"

    class Meta:
        db_table = 'app_profiles'
        verbose_name = 'Пациент'
        verbose_name_plural = 'Пациенты'

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(f"{self.insurance_policy}")
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('profile_detail', kwargs={'slug': self.slug})
