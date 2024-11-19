import pytest

from app_users.forms import RegisterUser, UserForm, ProfileForm
from app_users.models import Profile


@pytest.mark.django_db
def test_register_form_fields_label():
    form = RegisterUser()
    assert form.fields["username"].label == "Логин"
    assert form.fields["email"].label == "Электронная почта"
    assert form.fields["password1"].label == "Пароль"
    assert form.fields["password2"].label == "Повтор пароля"
    assert form.fields["first_name"].label == "ФИО"
    assert form.fields["image_avatar"].label == "Аватар"
    assert form.fields["number"].label == "Номер телефона"


@pytest.mark.django_db
def test_register_form_fields_required():
    form = RegisterUser()
    assert form.fields["image_avatar"].required is False


@pytest.mark.django_db
def test_register_form_fields_count():
    form = RegisterUser()
    assert len(form.fields) == 7


@pytest.mark.parametrize(
    "email, number, expected",
    [
        ("minaev.vad@yandex.ru", 89115550055, True),
        ("minaev.vad@yandex.ru", "something", False),
        ("vad", 89115550055, False),
    ],
)
@pytest.mark.django_db
def test_register_form(email, number, expected):
    data = {
        "username": "likeable",
        "email": email,
        "password1": "zoomer12345",
        "password2": "zoomer12345",
        "first_name": "Sox Mox Dox",
        "number": number,
        "image_avatar": "media.png",
    }
    form = RegisterUser(data=data)
    assert form.is_valid() is expected


@pytest.mark.django_db
def test_register_form_email_failed(user_factory):
    user_factory.create(email="minaev.vad@yandex.ru")
    data = {
        "username": "likeable",
        "email": "minaev.vad@yandex.ru",
        "password1": "zoomer12345",
        "password2": "zoomer12345",
        "first_name": "Sox Mox Dox",
        "number": 89115550055,
        "image_avatar": "media.png",
    }
    form = RegisterUser(data=data)
    assert form.is_valid() is False
    assert (
        "Пользователь с такой электронной почтой уже существует."
        in form.errors["email"]
    )


@pytest.mark.django_db
def test_user_form_fields_label():
    form = UserForm()
    assert form.fields["first_name"].label == "ФИО"
    assert form.fields["email"].label == "Электронная почта"


@pytest.mark.django_db
def test_register_form_fields_count():
    form = UserForm()
    assert len(form.fields) == 2


@pytest.mark.parametrize(
    "email, first_name, expected",
    [
        ("minaev.vad@yandex.ru", "Fox", True),
        ("vad", "Fox Dox Mox", False),
    ],
)
@pytest.mark.django_db
def test_user_form(email, first_name, expected):
    data = {
        "first_name": first_name,
        "email": email,
    }
    form = UserForm(data=data)
    assert form.is_valid() is expected


@pytest.mark.django_db
def test_profile_form_fields_label():
    form = ProfileForm()
    assert form.fields["number"].label == "Телефон"
    assert form.fields["image_avatar"].label == "Аватар"


@pytest.mark.django_db
def test_profile_form_fields_count():
    form = ProfileForm()
    assert len(form.fields) == 2


@pytest.mark.parametrize(
    "number, expected",
    [
        ("12345", True),
        (89115550055, True),
    ],
)
@pytest.mark.django_db
def test_profile_form(number, expected):
    data = {
        "number": number,
        "image_avatar": "media.png",
    }
    form = ProfileForm(data=data)
    assert form.is_valid() is expected


@pytest.mark.django_db
def test_profile_form_number_failed(user_factory):
    user = user_factory.create()
    profile = Profile.objects.get(user=user)
    profile.number = 89115550055
    profile.save()
    data = {
        "number": 89115550055,
        "image_avatar": "media.png",
    }
    form = ProfileForm(data=data)
    assert form.is_valid() is False
    assert "Пользователь с таким телефоном уже существует." in form.errors["number"]
