from django.contrib.auth.models import User
from django.db import models


class Profile(models.Model):
    """Модель дополнительной информации о пользователе."""

    user = models.OneToOneField(
        User,
        blank=True,
        on_delete=models.CASCADE,
        related_name="profiles",
        verbose_name="пользователь",
    )
    number = models.CharField(max_length=100, verbose_name="телефон")
    image_avatar = models.ImageField(
        upload_to="avatar_files/", blank=True, verbose_name="аватар"
    )

    objects = models.Manager()

    class Meta:
        verbose_name = "профиль"
        verbose_name_plural = "профили"
