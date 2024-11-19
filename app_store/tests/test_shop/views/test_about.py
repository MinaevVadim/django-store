import pytest
from django.urls import reverse


@pytest.mark.django_db
def test_about_successful(client):
    response = client.get(reverse("about"))
    assert response.status_code == 200
