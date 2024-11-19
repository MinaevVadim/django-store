import pytest

from app_order.forms import OrderForm, Payment


@pytest.mark.django_db
def test_order_form_fields_label():
    form = OrderForm()
    assert form.fields["name"].label == "название"
    assert form.fields["phone"].label == "номер телефона"
    assert form.fields["mail"].label == "электронная почта"
    assert form.fields["password"].label == "пароль"
    assert form.fields["passwordReply"].label == "повтор пароля"
    assert form.fields["delivery"].label == "доставка"
    assert form.fields["city"].label == "город"
    assert form.fields["address"].label == "адрес"
    assert form.fields["pay"].label == "оплата"


@pytest.mark.django_db
def test_order_form_fields_required():
    form = OrderForm()
    assert form.fields["password"].required is False
    assert form.fields["passwordReply"].required is False


@pytest.mark.django_db
def test_order_form_fields_count():
    form = OrderForm()
    assert len(form.fields) == 9


@pytest.mark.django_db
def test_order_form():
    data = {
        "name": "order1",
        "phone": 89115550055,
        "mail": "zoomer12345",
        "password": "zoomer12345",
        "passwordReply": "Sox Mox Dox",
        "delivery": "delivery",
        "city": "SPB",
        "address": "address",
        "pay": "cash",
    }
    form = OrderForm(data=data)
    assert form.is_valid() is True


@pytest.mark.django_db
def test_payment_form_fields_required():
    form = Payment()
    assert form.fields["generic_number"].required is False


@pytest.mark.django_db
def test_payment_form_fields_count():
    form = Payment()
    assert len(form.fields) == 2


@pytest.mark.parametrize(
    "number, expected",
    [
        (12345, False),
        (22244422, True),
        (2244, True),
        (4424242, True),
        (11111, False),
        (0, True),
        (1, False),
    ],
)
@pytest.mark.django_db
def test_payment_form(number, expected):
    data = {
        "card_number": number,
        "generic_number": number,
    }
    form = Payment(data=data)
    assert form.is_valid() is expected
