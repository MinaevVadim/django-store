from django.contrib.auth.models import User
from django.db import models
from mptt.fields import TreeForeignKey
from mptt.models import MPTTModel

from utils.abstract_models import SoftIsDelete
from utils.managers import SoftDeleteManager

ACTIVE = (
        ('1', 'active'),
        ('2', 'inactive'),
    )


class Product(SoftIsDelete):
    """Модель продуктов."""

    name = models.CharField(
        max_length=1000,
        db_index=True,
        verbose_name='название товара'
    )
    description = models.TextField(
        max_length=10000,
        verbose_name='описание товара'
    )
    price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0,
        blank=True,
        verbose_name='цена товара'
    )
    count_reviews = models.IntegerField(
        default=0,
        verbose_name='количество отзывов'
    )
    tags = models.ManyToManyField(
        'Tag',
        blank=True,
        related_name='tags_products'
    )
    category = TreeForeignKey(
        'Category',
        blank=True,
        on_delete=models.PROTECT,
        related_name='category_products',
        verbose_name='категория'
    )
    limited_edition = models.BooleanField(
        verbose_name='ограниченный тираж'
    )
    count_goods = models.IntegerField(
        verbose_name='количество товара'
    )
    free_delivery = models.BooleanField(
        default=False,
        verbose_name='бесплатная доставка'
    )
    number_of_purchases = models.IntegerField(
        default=0,
        verbose_name='количество покупок товара'
    )
    active_product = models.BooleanField(
        verbose_name='активность товара'
    )
    date_product = models.DateTimeField(
        auto_now_add=True,
        verbose_name='дата поступления товара'
    )
    objects = SoftDeleteManager()

    def __str__(self):
        return str(self.name)

    class Meta:
        ordering = ['name', 'number_of_purchases']
        verbose_name = 'товар'
        verbose_name_plural = 'товары'


class Tag(models.Model):
    """Модель тега."""

    name = models.CharField(
        max_length=1000,
        verbose_name='название тега'
    )

    def __str__(self):
        return str(self.name)

    class Meta:
        verbose_name = 'тег'
        verbose_name_plural = 'теги'


class Category(MPTTModel, SoftIsDelete):
    """Модель категории."""

    name = models.CharField(
        max_length=1000,
        db_index=True,
        verbose_name='название категории'
    )
    parent = TreeForeignKey(
        'self',
        null=True,
        on_delete=models.PROTECT,
        blank=True,
        verbose_name='родительская категория'
    )
    active_category = models.CharField(
        max_length=1,
        choices=ACTIVE,
        default='1',
        blank=True,
        verbose_name='автивность категории'
    )
    file_icon = models.FileField(
        upload_to='files_icon/',
        null=True,
        blank=True,
        verbose_name='файл иконки'
    )
    objects = SoftDeleteManager()

    def __str__(self):
        return str(self.name)

    class Meta:
        ordering = ['name']
        verbose_name = 'категория'
        verbose_name_plural = 'категории'


class Comment(models.Model):
    """Модель комментария."""

    name_user = models.CharField(
        max_length=100,
        verbose_name='имя пользователя',
        blank=True
    )
    text_comment = models.TextField(
        max_length=10000,
        verbose_name='текст комментария'
    )
    product = models.ForeignKey(
        'Product',
        blank=True,
        null=True,
        on_delete=models.CASCADE,
        related_name='product_comments',
        verbose_name='продукт'
    )
    user = models.ForeignKey(
        User,
        blank=True,
        null=True,
        on_delete=models.CASCADE,
        related_name='user_comments',
        verbose_name='пользователь'
    )
    date_comment = models.DateTimeField(
        auto_now_add=True,
        verbose_name='дата комментария'
    )

    def __str__(self):
        return 'user: %s | date: %s' % (self.user, self.date_comment)

    class Meta:
        verbose_name = 'комментарий'
        verbose_name_plural = 'комментарии'


class FileProduct(models.Model):
    """Модель изображений товара."""

    product_file = models.ForeignKey(
        'Product',
        null=True,
        on_delete=models.CASCADE,
        related_name='file_products',
        verbose_name='продукт'
    )
    files = models.FileField(
        upload_to='files_goods/',
        verbose_name='файл'
    )

    class Meta:
        verbose_name = 'файл продукта'
        verbose_name_plural = 'файлы продукта'

