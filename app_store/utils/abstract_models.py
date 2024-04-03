from django.db import models


class SoftIsDelete(models.Model):
    """
    Абстрактая модель для добавления
    функционала мягкого удаления объекта.
    """

    is_delete = models.BooleanField(default=False)

    def soft_delete(self):
        """Метод изменения флага is_delete."""
        self.is_delete = True
        self.save()

    class Meta:
        abstract = True
