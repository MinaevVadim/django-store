import pytest
from django.urls import reverse


@pytest.mark.django_db
def test_account_successful(admin_client):
    response = admin_client.get(reverse("account"))
    assert response.status_code == 200


@pytest.mark.django_db
def test_account_redirect(client):
    response = client.get(reverse("account"))
    assert response.status_code == 302


@pytest.mark.django_db
def test_login_account_successful(auto_login_user):
    client, user = auto_login_user()
    response = client.get(reverse("account"))
    first_name_encoded = user.first_name.encode()
    assert response.status_code == 200
    assert response.context["object_list"].first().username == user.username
    assert first_name_encoded in response.content
