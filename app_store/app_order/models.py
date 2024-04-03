from django.contrib.auth.models import User
from django.db import models

from app_shop.models import Product
from utils.abstract_models import SoftIsDelete
from utils.managers import SoftDeleteManager

METHOD_PAYMENT = (
        ('online', 'Онлайн картой'),
        ('someone', 'Онлайн со случайного чужого счёта')
    )
DELIVERY_METHOD = (
        ('ordinary', 'Обычная доставка'),
        ('express', 'Экспресс-доставка')
    )
STATUS_PAYMENT = (
    ('True', 'не оплачен'),
    ('False', 'оплачен')
)


class ProductOrder(models.Model):
    """Промежуточная модель продуктов и заказов"""
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
    )
    order = models.ForeignKey(
        'Order',
        on_delete=models.CASCADE,
    )
    count = models.IntegerField(
        default=0,
        verbose_name='количество товара',
    )
    price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name='стоимость товара'
    )


class Order(SoftIsDelete):
    """Модель заказа."""

    products = models.ManyToManyField(
        Product,
        through=ProductOrder,
        related_name='orders',
    )
    user = models.ForeignKey(
        User,
        blank=True,
        on_delete=models.CASCADE,
        related_name='orders',
        verbose_name='пользователь',
    )
    delivery_method = models.CharField(
        max_length=10,
        choices=DELIVERY_METHOD,
        default='ordinary',
        verbose_name='способ доставки'
    )
    city = models.CharField(
        max_length=50,
        verbose_name='город',
    )
    address = models.CharField(
        max_length=1000,
        verbose_name='адрес',
    )
    payment_method = models.CharField(
        max_length=10,
        choices=METHOD_PAYMENT,
        default='online',
        verbose_name='способ оплаты',
    )
    order_number = models.IntegerField(
        blank=True,
        verbose_name='номер заказа',
    )
    status = models.CharField(
        max_length=10,
        choices=STATUS_PAYMENT,
        default='True',
        verbose_name='статус оплаты',
    )
    commentary = models.TextField(
        max_length=1000,
        blank=True,
        verbose_name='комментарии к заказу',
    )

    date_order = models.DateTimeField(
        auto_now_add=True,
        verbose_name='дата заказа',
    )
    error_text = models.CharField(
        max_length=1000,
        blank=True,
        verbose_name='текст ошибки',
    )
    sum_order = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0,
        blank=True,
        verbose_name='сумма заказа',
    )
    objects = SoftDeleteManager()

    def __str__(self):
        return str(self.id)

    class Meta:
        verbose_name = 'заказ'
        verbose_name_plural = 'заказы'
