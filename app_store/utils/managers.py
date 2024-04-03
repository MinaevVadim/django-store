from django.db import models
from django.db.models import F


class SoftDeleteManager(models.Manager):
    """
    Менеджер для фильтрации не удаленных объектов
    и общий оптимизированный запрос для продуктов.
    """

    def get_queryset(self) -> 'get_queryset':
        if self.model.__name__ == 'Product':
            return super().get_queryset().filter(
                is_delete=False).annotate(
                file=F('file_products__files')
            ).only('id', 'name', 'price', 'description', 'category').distinct('name')
        return super().get_queryset().filter(is_delete=False)
