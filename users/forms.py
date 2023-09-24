from django import forms
from django.contrib.auth.forms import UserChangeForm, UserCreationForm
from users.models import User


class FormStyleMixin:
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update({
                'class': 'form-control',
                'autocomplete': 'off'
            })


class UserForm(FormStyleMixin, UserChangeForm):
    class Meta:
        model = User
        fields = ('email', 'first_name', 'last_name', 'phone', 'photo')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['password'].widget = forms.HiddenInput()


class UserRegisterForm(FormStyleMixin, UserCreationForm):
    """Форма регистрации пользователя"""
    class Meta:
        model = User
        fields = ('email', 'password1', 'password2')


class UserUpdateForm(FormStyleMixin, forms.ModelForm):
    class Meta:
        model = User
        fields = (
            'email', 'first_name', 'middle_name', 'last_name', 'slug',
            'birth_date', 'gender', 'phone', 'blood_group', 'city'
        )

    def clean_email(self):
        email = self.cleaned_data.get('email')
        username = self.cleaned_data.get('username')
        if email and User.objects.filter(email=email)\
                .exclude(username=username).exists():
            raise forms.ValidationError('Email адрес должен быть уникальным')
        return email
