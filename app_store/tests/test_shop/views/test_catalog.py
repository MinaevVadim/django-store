import pytest
from django.urls import reverse

from app_shop.filters import MyFilter


@pytest.mark.django_db
def test_get_catalog_successful(client):
    response = client.get(reverse("catalog"))
    assert response.status_code == 200


@pytest.mark.django_db
def test_existed_catalog_products(client, product_factory, tag_factory):
    tags = tag_factory.create_batch(3)
    product_factory.create_batch(15, tags=tags)
    response = client.get(reverse("catalog"))
    assert response.context["products"].count() == 6
    assert response.context["tags"].count() == 3
    assert isinstance(response.context["filter"], MyFilter)
