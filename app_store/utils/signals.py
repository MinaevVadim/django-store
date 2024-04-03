from django.core.cache import cache
from django.db.models.signals import post_save
from django.dispatch import receiver

from app_shop.models import Product


@receiver(post_save, sender=Product)
def post_save_product(**kwargs) -> None:
    """Сигнал сброса кэша после изменения объекта товара."""
    instance = kwargs['instance']
    cache.delete('key_product_%s' % instance.id)
