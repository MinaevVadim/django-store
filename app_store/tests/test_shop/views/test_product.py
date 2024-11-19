import pytest
from django.urls import reverse


@pytest.mark.django_db
def test_product_successful(client, product_factory):
    product = product_factory.create()
    response = client.get(reverse("product", kwargs={"pk": product.pk}))
    assert response.status_code == 200


@pytest.mark.django_db
def test_context_product_successful(
    client, user_factory, comment_factory, tag_factory, product_factory
):
    tags = tag_factory.create_batch(1)
    product = product_factory.create(tags=tags)
    user = user_factory.create()
    comment_factory.create(product=product, user=user)
    response = client.get(reverse("product", kwargs={"pk": product.pk}))
    assert response.status_code == 200
    assert response.context["product"]
    assert response.context["posts"].count() == 1
    assert response.context["tags"].count() == 1
    assert response.context["count_reviews"] == 1
