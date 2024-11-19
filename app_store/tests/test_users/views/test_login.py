import pytest
from django.urls import reverse


@pytest.mark.django_db
def test_login_expected_code_successful(client):
    response = client.get(reverse("login_user"))
    assert response.status_code == 200


@pytest.mark.django_db
def test_login_account_successful(auto_login_user): ...
