from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import SetPasswordForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.contrib.auth.views import LoginView, PasswordChangeView
from django.contrib.messages.views import SuccessMessageMixin
from django.core.mail import send_mail
from django.forms import forms
from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect, render
from django.urls import reverse
from django.views.generic import CreateView, ListView

from app_order.models import Order
from app_users.forms import RegisterUser, RestorePasswordForm, UserForm, ProfileForm
from app_users.models import Profile


def restore_password(request: HttpRequest) -> HttpResponse:
    """Функция представление восстановления пароля."""
    form_email = RestorePasswordForm(request.POST or None)
    if form_email.is_valid():
        res_password = User.objects.make_random_password()
        user_email = form_email.cleaned_data.get('user_email')
        user = User.objects.filter(email=user_email).first()
        if user:
            user.set_password(res_password)
            user.save()
            send_mail(
                subject='Восстановление пароля',
                message=f'Ваш новый пароль: {res_password}',
                from_email='admin@mail.ru',
                recipient_list=[user_email]
            )
    return render(
        request,
        'app_users/restore_password.html',
        context={'form': form_email}
    )


class UpdatePassword(
    LoginRequiredMixin,
    SuccessMessageMixin,
    PasswordChangeView
):
    """Класс представление изменения пароля пользователя."""

    login_url = '/login/'
    form_class = SetPasswordForm
    template_name = 'app_users/change_password.html'
    success_message = 'Пароль успешно изменен!'

    def get_success_url(self):
        """
        Переопределитель генерации url, на который будет
        совершен переход, если форма смены пароля валидна.
        """
        return reverse('profile', args=[self.request.user.pk])


class LoginUserView(LoginView):
    """Класс представление аутентификации пользователя."""

    model = User
    template_name = 'app_users/login.html'

    def get_redirect_url(self):
        return self.request.META.get('HTTP_REFERER')


def logout_function(request: HttpRequest) -> HttpResponse:
    """Класс представление выхода пользователия из системы."""
    logout(request)
    return redirect(reverse('main'))


class AccountList(LoginRequiredMixin, ListView):
    """Класс представление аккаунта пользователя."""

    login_url = '/login/'
    model = User
    template_name = 'app_users/account.html'

    def get_context_data(self, *, object_list=None, **kwargs) -> dict:
        """
        Метод объединения данных контекста всех родительских
        классов с данными истории заказов.
        """
        context = super().get_context_data(**kwargs)
        context['order_history'] = Order.objects.only(
            'delivery_method',
            'payment_method',
            'sum_order',
            'status',
            'error_text',
            'order_number',
            'date_order',
        ).filter(user=self.request.user).last()
        return context


class RegisterList(CreateView):
    """Класс представление регистрации пользователя."""

    form_class = RegisterUser
    template_name = 'app_users/registration.html'

    def form_valid(self, form: forms) -> HttpResponse:
        """Метод получения данных формы регистрации и их обработка."""
        user_form = form.save(commit=False)
        user_form.save()
        Profile.objects.create(
            user=user_form,
            number=form.cleaned_data.get('number'),
            image_avatar=form.cleaned_data.get('image_avatar'),
        )
        new_user = authenticate(
            username=form.cleaned_data.get('username'),
            password=form.cleaned_data.get('password1'))
        login(self.request, new_user)
        return redirect(reverse('main'))


@login_required
def update_user_profile(request: HttpRequest) -> HttpResponse:
    if request.method == 'POST':
        form_user = UserForm(request.POST, instance=request.user)
        form_profile = ProfileForm(request.POST, request.FILES, instance=request.user.profiles)
        if form_user.is_valid() and form_profile.is_valid():
            form_user.save()
            form_profile.save()
        return redirect(reverse('profile'))
    else:
        form_user = UserForm(instance=request.user)
        form_profile = ProfileForm(instance=request.user.profiles)
    return render(
        request=request,
        template_name='app_users/profile.html',
        context={'form': form_user, 'form_profile': form_profile},
    )
