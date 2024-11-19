import pytest
from django.urls import reverse


@pytest.mark.django_db
def test_logout_expected_code_successful(client):
    response = client.get(reverse("logout"))
    assert response.status_code == 302


@pytest.mark.django_db
def test_logout_account_successful(auto_login_user):
    client, user = auto_login_user()
    client.get(reverse("logout"))
    response = client.get(reverse("account"))
    assert response.status_code == 302
