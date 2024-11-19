import pytest
from django.urls import reverse


@pytest.mark.django_db
def test_restore_password_expected_code_successful(client):
    response = client.get(reverse("restore_password"))
    assert response.status_code == 200
