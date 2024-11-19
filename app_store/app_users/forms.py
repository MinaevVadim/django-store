from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from app_users.models import Profile
from utils.validators_forms import image_size


class RegisterUser(UserCreationForm):
    """Форма для регистрации пользователя."""

    username = forms.CharField(label="Логин")
    email = forms.EmailField(label="Электронная почта")
    password1 = forms.CharField(label="Пароль", widget=forms.PasswordInput)
    password2 = forms.CharField(label="Повтор пароля", widget=forms.PasswordInput)
    first_name = forms.CharField(label="ФИО")
    number = forms.IntegerField(label="Номер телефона")
    image_avatar = forms.FileField(
        label="Аватар", validators=[image_size], required=False
    )

    class Meta:
        model = User
        fields = [
            "username",
            "first_name",
            "email",
            "password1",
            "password2",
            "number",
            "image_avatar",
        ]

    def clean_email(self):
        """Метод валидации электронной почты."""
        email = self.cleaned_data.get("email")
        if email and User.objects.filter(email=email).exists():
            raise forms.ValidationError(
                "Пользователь с такой электронной почтой уже существует."
            )
        return email


class UserForm(forms.ModelForm):
    """Форма пользователя."""

    first_name = forms.CharField(
        label="ФИО", max_length=100, widget=forms.TextInput(attrs={"size": "50"})
    )
    email = forms.EmailField(
        label="Электронная почта",
        widget=forms.EmailInput(attrs={"class": "form-input"}),
    )

    class Meta:
        model = User
        fields = ["first_name", "email"]


class ProfileForm(forms.ModelForm):
    """Форма профайла пользователя."""

    number = forms.CharField(
        label="Телефон", widget=forms.TextInput(attrs={"class": "form-input"})
    )
    image_avatar = forms.ImageField(
        label="Аватар",
        required=False,
        validators=[image_size],
    )

    class Meta:
        model = Profile
        fields = ["number", "image_avatar"]

    def clean_number(self):
        """Метод валидации номера телефона."""
        number = self.cleaned_data.get("number")
        if number and Profile.objects.filter(number=number).exists():
            raise forms.ValidationError(
                "Пользователь с таким телефоном уже существует."
            )
        return number


class RestorePasswordForm(forms.Form):
    """Форма восстановления пароля через электронную почту."""

    user_email = forms.EmailField(label="Электронная почта")
