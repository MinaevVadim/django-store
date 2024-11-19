import pytest
from django.urls import reverse


@pytest.mark.django_db
def test_registration_expected_code_successful(client):
    response = client.get(reverse("register_user"))
    assert response.status_code == 200
