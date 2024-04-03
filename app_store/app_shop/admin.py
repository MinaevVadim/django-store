from django.contrib import admin
from mptt.admin import MPTTModelAdmin

from utils.mixins import UpdateDeleteDMixin
from .models import Category, Comment, FileProduct, Product, Tag


class ShopTagM2M(admin.StackedInline):
    model = Product.tags.through


class TagShop(admin.ModelAdmin):
    """
    Класс TagShop для изменения отображения модели
    Tag в пользовательском интерфейсе админ-панели.
    """

    list_display = ['id', 'name']
    list_filter = ['id', 'name']
    inlines = [ShopTagM2M]


class CategoryShop(UpdateDeleteDMixin, MPTTModelAdmin, admin.ModelAdmin):
    """
    Класс CategoryShop для изменения отображения
    модели Category в пользовательском интерфейсе админ-панели.
    """
    my_model = 'категории'
    changer = 'app_shop_category'
    list_display = [
        'id',
        'name',
        'active_category',
        'update_obj',
        'delete_obj',
    ]
    list_filter = ['id', 'active_category']


class CommentShop(UpdateDeleteDMixin, admin.ModelAdmin):
    """
    Класс CommentShop для изменения отображения модели
    Comment в пользовательском интерфейсе админ-панели.
    """
    my_model = 'комментария'
    changer = 'app_shop_comment'
    list_display = [
        'id',
        'name_user',
        'text_comment',
        'product',
        'user',
        'update_obj',
        'delete_obj',
    ]
    list_filter = ['id', 'product']


class CartShop(admin.ModelAdmin):
    """
    Класс CartShop для изменения отображения модели
    Cart в пользовательском интерфейсе админ-панели.
    """

    list_display = ['id', 'product', 'user_auth', 'session']
    list_filter = ['id', 'product', 'user_auth']


class FileProductAdmin(admin.StackedInline):
    """
    Класс FileProductAdmin для изменения отображения модели
    FileProduct в пользовательском интерфейсе админ-панели.
    """

    model = FileProduct


class ProductShop(UpdateDeleteDMixin, admin.ModelAdmin):
    """
    Класс ProductShop для изменения отображения модели
    Product в пользовательском интерфейсе админ-панели.
    """
    my_model = 'продукта'
    changer = 'app_shop_product'
    list_display = [
        'id',
        'name',
        'date_product',
        'get_text_description',
        'price',
        'count_reviews',
        'limited_edition',
        'free_delivery',
        'update_obj',
        'delete_obj',
    ]
    search_fields = ['id', 'name']
    list_editable = ['limited_edition', 'free_delivery']
    inlines = [FileProductAdmin]
    list_filter = [
        'id',
        'limited_edition',
        'free_delivery',
    ]

    def get_text_description(self, obj):
        """Метод сокращения вывода текста до 15 букв."""
        if len(obj.description) > 15:
            return obj.description[:15] + '...'
        else:
            return obj.description

    get_text_description.short_description = "Описание товара"


class ProductFileAdmin(admin.ModelAdmin):
    """
    Класс ProductFileAdmin для изменения отображения
    модели FileProduct в пользовательском интерфейсе админ-панели.
    """

    list_display = ['id', 'files']
    list_filter = ['id']


admin.site.register(Tag, TagShop)
admin.site.register(Product, ProductShop)
admin.site.register(Category, CategoryShop)
admin.site.register(Comment, CommentShop)
admin.site.register(FileProduct, ProductFileAdmin)
