import pytest
from django.urls import reverse


@pytest.mark.django_db
@pytest.mark.parametrize("url", ["main", "login_user", "order"])
def test_context_processor_successful(client, category_factory, url):
    category_factory.create_batch(5)
    response = client.get(reverse(url))
    assert response.status_code == 200
    assert response.context["categories"].count() == 5
