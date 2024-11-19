import pytest


@pytest.mark.django_db
def test_order_verbose_name_fields(create_order):
    order, _, _ = create_order
    assert order._meta.get_field("delivery_method").verbose_name == "способ доставки"
    assert order._meta.get_field("order_number").verbose_name == "номер заказа"
    assert order._meta.get_field("status").verbose_name == "статус оплаты"
    assert order._meta.get_field("commentary").verbose_name == "комментарии к заказу"
    assert order._meta.get_field("date_order").verbose_name == "дата заказа"
    assert order._meta.get_field("error_text").verbose_name == "текст ошибки"
    assert order._meta.get_field("city").verbose_name == "город"
    assert order._meta.get_field("address").verbose_name == "адрес"
    assert order._meta.get_field("payment_method").verbose_name == "способ оплаты"
    assert order._meta.get_field("sum_order").verbose_name == "сумма заказа"


@pytest.mark.django_db
def test_order_length_fields(create_order):
    order, _, _ = create_order
    assert order._meta.get_field("delivery_method").max_length == 10
    assert order._meta.get_field("status").max_length == 10
    assert order._meta.get_field("commentary").max_length == 1000
    assert order._meta.get_field("error_text").max_length == 1000
    assert order._meta.get_field("city").max_length == 50
    assert order._meta.get_field("address").max_length == 1000
    assert order._meta.get_field("payment_method").max_length == 10


@pytest.mark.django_db
def test_order_blank_fields(create_order):
    order, _, _ = create_order
    assert order._meta.get_field("user").blank is True
    assert order._meta.get_field("order_number").blank is True
    assert order._meta.get_field("commentary").blank is True
    assert order._meta.get_field("date_order").blank is True
    assert order._meta.get_field("error_text").blank is True
    assert order._meta.get_field("sum_order").blank is True


@pytest.mark.django_db
def test_order_meta_verbose_table(create_order):
    order, _, _ = create_order
    assert order._meta.verbose_name == "заказ"
    assert order._meta.verbose_name_plural == "заказы"


@pytest.mark.django_db
def test_order_for_date_time_field(create_order):
    order, _, _ = create_order
    assert order._meta.get_field("date_order").auto_now_add is True
