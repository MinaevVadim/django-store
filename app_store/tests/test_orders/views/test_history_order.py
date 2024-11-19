import pytest
from django.urls import reverse


@pytest.mark.django_db
def test_history_with_login_code_successful(auto_login_user, create_order):
    client, _ = auto_login_user()
    order, _, _ = create_order
    response = client.get(reverse("history_order"))
    assert response.status_code == 200
    assert str(order.order_number) in response.content.decode()
    assert order in response.context["orders"]


@pytest.mark.django_db
def test_history_order_without_login_successful(client):
    response = client.get(reverse("history_order"))
    assert response.status_code == 302
