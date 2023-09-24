from django.contrib.auth import login
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.views import View
from django.views.generic import (
    CreateView, TemplateView, DetailView, UpdateView)
from django.contrib.auth.views import LoginView
from django.db import transaction

from core import settings

from users.forms import UserRegisterForm, UserUpdateForm
from users.models import User


class TitleMixin:
    title = ''

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = self.title
        return context


class UserRegisterView(TitleMixin, CreateView):
    """Реализация регистрации пользователя"""
    model = User
    form_class = UserRegisterForm
    success_url = reverse_lazy('users:login')
    template_name = 'users/user_register.html'
    success_message = 'Вы успешно подписались. Проверьте почту для активации!'
    title = 'Регистрация на сайте'

    def form_valid(self, form):
        self.object = form.save()
        token = default_token_generator.make_token(self.object)
        uid = urlsafe_base64_encode(force_bytes(self.object.pk))
        activation_url = reverse_lazy('users:confirm_email',
                                      kwargs={'uidb64': uid, 'token': token})

        send_mail(
            subject='Подтверждение почты',
            message=(
                'Для подтверждения регистрации перейдите по ссылке: '
                'http://localhost:8000/{activation_url}'
            ),
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[self.object.email],
            fail_silently=False
        )
        return redirect('users:email_confirmation_sent')


class UserConfirmEmailView(View):
    """Реализация подтверждения регистрации пользователя через email"""

    def get(self, request, uidb64, token):
        try:
            uid = urlsafe_base64_decode(uidb64)
            user = User.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            user = None

        if user is not None and default_token_generator.check_token(user,
                                                                    token):
            user.is_active = True
            user.save()
            login(request, user)
            return redirect('users:email_confirmed')
        else:
            return redirect('users:email_confirmation_failed')


class EmailConfirmationSentView(TitleMixin, TemplateView):
    """Реализация отправки email подтверждения регистрации пользователя"""
    template_name = 'users/email_confirmation_sent.html'
    title = 'Письмо активации отправлено'


class EmailConfirmedView(TitleMixin, TemplateView):
    """Реализация вида подтверждения регистрации пользователя"""
    template_name = 'users/email_confirmed.html'
    title = 'Ваш электронный адрес активирован'


class EmailConfirmationFailedView(TitleMixin, TemplateView):
    """Реализация вида неуспешной регистрации пользователя"""
    template_name = 'users/email_confirmation_failed.html'
    title = 'Ваш электронный адрес не активирован'


class CustomLoginView(LoginView):
    template_name = 'users/login.html'

    def get_success_url(self):
        return reverse_lazy('main:home')


class UserDetailView(DetailView):
    model = User
    context_object_name = 'user'
    template_name = 'users/profile_detail.html'

    def get(self, request, *args, **kwargs):
        user = User.objects.get(slug=kwargs['slug'])
        return render(request, 'users/profile_detail.html',
                      {'slug': user.slug})


class UserUpdateView(UpdateView):
    model = User
    form_class = UserUpdateForm
    template_name = 'users/profile_edit.html'

    def get_object(self, queryset=None):
        return self.request.user

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = (
            f'Редактирование профиля пользователя: {self.object.slug}'
        )
        if self.request.POST:
            context['user_form'] = UserUpdateForm(
                self.request.POST, instance=self.request.user
            )
        else:
            context['user_form'] = UserUpdateForm(instance=self.request.user)
        return context

    def form_valid(self, form):
        context = self.get_context_data()
        user_form = context['user_form']
        with transaction.atomic():
            if all([form.is_valid(), user_form.is_valid()]):
                user_form.save()
                form.save()
            else:
                context.update({'user_form': user_form})
                return self.render_to_response(context)
        return super(UserUpdateView, self).form_valid(form)

    def get_success_url(self):
        return reverse_lazy('user:profile_detail',
                            kwargs={'slug': self.object.slug})
