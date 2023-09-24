from django.test import TestCase
from django.core.exceptions import ValidationError
from users.models import User
from users.forms import UserRegisterForm, UserUpdateForm

class UserModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        # Создание пользователя
        User.objects.create(first_name='Иван', middle_name='Иванович', last_name='Иванов', email='ivanov@example.com', insurance_policy='1234567890', gender='Мужской', blood_group='A+')

    def test_first_name_label(self):
        user = User.objects.get(id=1)
        field_label = user._meta.get_field('first_name').verbose_name
        self.assertEquals(field_label, 'Имя')

    def test_email_unique(self):
        user = User.objects.get(id=1)
        field_unique = user._meta.get_field('email').unique
        self.assertTrue(field_unique)

    def test_slug_creation(self):
        user = User.objects.get(id=1)
        self.assertEquals(user.slug, '1234567890')

    def test_get_absolute_url(self):
        user = User.objects.get(id=1)
        # Проверка, что get_absolute_url возвращает правильный url
        self.assertEquals(user.get_absolute_url(), '/user/1234567890/')

    def test_user_register_form(self):
        form_data = {'email': 'test@example.com', 'password1': 'password123', 'password2': 'password123'}
        form = UserRegisterForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_user_update_form(self):
        form_data = {'email': 'test@example.com', 'first_name': 'Тест', 'middle_name': 'Тестович', 'last_name': 'Тестов', 'slug': 'testov', 'birth_date': '2000-01-01', 'gender': 'Мужской', 'phone': '+79161234567', 'blood_group': 'A+', 'city': 'Москва'}
        form = UserUpdateForm(data=form_data)
        self.assertTrue(form.is_valid())

    # Добавьте здесь больше тестов для других полей и методов...
