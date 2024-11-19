import pytest


@pytest.mark.django_db
def test_profile_verbose_name_fields(create_user_profile):
    _, profile = create_user_profile
    assert profile._meta.get_field("number").verbose_name == "телефон"
    assert profile._meta.get_field("image_avatar").verbose_name == "аватар"


@pytest.mark.django_db
def test_profile_length_fields(create_user_profile):
    _, profile = create_user_profile
    assert profile._meta.get_field("number").max_length == 100


@pytest.mark.django_db
def test_profile_blank_fields(create_user_profile):
    _, profile = create_user_profile
    assert profile._meta.get_field("user").blank is True
    assert profile._meta.get_field("image_avatar").blank is True


@pytest.mark.django_db
def test_profile_upload_to_field(create_user_profile):
    _, profile = create_user_profile
    assert profile._meta.get_field("image_avatar").upload_to == "avatar_files/"


@pytest.mark.django_db
def test_profile_meta_verbose_table(create_user_profile):
    _, profile = create_user_profile
    assert profile._meta.verbose_name == "профиль"
    assert profile._meta.verbose_name_plural == "профили"
