import pytest
from django.urls import reverse


@pytest.mark.django_db
def test_change_password_expected_code_no_login_successful(client):
    response = client.get(reverse("change_password"))
    assert response.status_code == 302


@pytest.mark.django_db
def test_change_password_expected_code_with_login_successful(auto_login_user):
    client, user = auto_login_user()
    response = client.get(reverse("change_password"))
    assert response.status_code == 200
