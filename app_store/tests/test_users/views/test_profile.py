import pytest
from django.urls import reverse


@pytest.mark.django_db
def test_login_expected_code_no_login_profile(client):
    response = client.get(reverse("profile"))
    assert response.status_code == 302


@pytest.mark.django_db
def test_login_expected_code_with_login_profile(auto_login_user):
    client, user = auto_login_user()
    response = client.get(reverse("profile"))
    assert response.status_code == 200
