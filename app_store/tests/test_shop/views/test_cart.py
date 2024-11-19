import pytest
from django.urls import reverse


@pytest.mark.django_db
def test_cart_successful(client, product_factory):
    product = product_factory.create()
    client.get(reverse("cart", kwargs={"product_id": product.pk}))
    response = client.get(reverse("cart_user"))
    assert response.status_code == 200
