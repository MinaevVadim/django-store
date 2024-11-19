import pytest
from django.urls import reverse


@pytest.mark.django_db
def test_order_expected_code_successful(client):
    response = client.get(reverse("order"))
    assert response.status_code == 200


@pytest.mark.django_db
def test_order_with_login(auto_login_user):
    client, user = auto_login_user()
    response = client.get(reverse("order"))
    assert (
        "Чтобы сделать заказ, вам необходимо авторизоваться"
        not in response.content.decode()
    )


@pytest.mark.django_db
def test_order_without_login(client):
    response = client.get(reverse("order"))
    assert (
        "Чтобы сделать заказ, вам необходимо авторизоваться"
        in response.content.decode()
    )
