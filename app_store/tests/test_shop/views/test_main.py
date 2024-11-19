import pytest
from django.urls import reverse


@pytest.mark.django_db
def test_get_main_list_successful(client):
    response = client.get(reverse("main"))
    assert response.status_code == 200


@pytest.mark.django_db
def test_existed_products(client, product_factory):
    product_factory.create_batch(15)
    response = client.get(reverse("main"))
    assert response.context["product_list"].count() == 15
    assert response.context["favorites"].count() == 3
    assert response.context["populars"].count() == 9
    check_limited_edition = all(
        [x.limited_edition for x in response.context["limited_edition"]]
    )
    assert check_limited_edition is True
