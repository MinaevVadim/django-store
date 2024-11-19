from random import choice
from string import ascii_lowercase

import pytest

from app_shop.forms import UserComment, CountProductCart

BIG_TEXT = "".join([choice(ascii_lowercase) for _ in range(11000)])


@pytest.mark.django_db
def test_user_comment_form_fields_label():
    form = UserComment()
    assert form.fields["name_user"].label == "Имя пользователя"
    assert form.fields["text_comment"].label == "Текст комментария"


@pytest.mark.django_db
def test_user_comment_fields_count():
    form = UserComment()
    assert len(form.fields) == 2


@pytest.mark.parametrize(
    "text, expected",
    [
        (BIG_TEXT, False),
        ("text", True),
    ],
)
@pytest.mark.django_db
def test_user_comment_form(text, expected):
    data = {
        "name_user": "likeable",
        "text_comment": text,
    }
    form = UserComment(data=data)
    assert form.is_valid() is expected


@pytest.mark.django_db
def test_count_product_cart_form_fields_label():
    form = CountProductCart()
    assert form.fields["count_good_basket"].label == "Количество"


@pytest.mark.django_db
def test_count_product_cart_fields_count():
    form = CountProductCart()
    assert len(form.fields) == 1
