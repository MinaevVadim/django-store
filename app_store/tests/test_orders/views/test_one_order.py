import pytest
from django.urls import reverse


@pytest.mark.django_db
def test_order_with_login_and_status_code(auto_login_user, create_order):
    client, _ = auto_login_user()
    order, user, _ = create_order
    response = client.get(reverse("one_order", kwargs={"order_id": order.pk}))
    assert response.status_code == 200
    assert order.address in response.content.decode()
    assert order.city in response.content.decode()
    assert user.email in response.content.decode()


@pytest.mark.django_db
def test_order_without_login_and_status_code(client, create_order):
    order, user, _ = create_order
    response = client.get(reverse("one_order", kwargs={"order_id": order.pk}))
    assert response.status_code == 302
