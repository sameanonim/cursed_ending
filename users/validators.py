from django.core.validators import (RegexValidator, EmailValidator,
                                    FileExtensionValidator)

NULLABLE = {'blank': True, 'null': True}

GENDER_CHOICES = [
    ('М', 'Мужской'),
    ('Ж', 'Женский'),
]

BLOOD_GROUP_CHOICES = [
    ('A+', 'A+'),
    ('A-', 'A-'),
    ('B+', 'B+'),
    ('B-', 'B-'),
    ('AB+', 'AB+'),
    ('AB-', 'AB-'),
    ('O+', 'O+'),
    ('O-', 'O-'),
]

phone_validator = RegexValidator(
    regex=r'^\+?\d{10,15}$',
    message='Введите корректный номер телефона'
)

email_validator = EmailValidator(
    message='Введите корректный адрес электронной почты'
)

image_validator = FileExtensionValidator(
    allowed_extensions=('png', 'jpg', 'jpeg')
)
