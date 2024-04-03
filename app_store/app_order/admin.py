from django.contrib import admin

from app_order.models import Order
from utils.mixins import UpdateDeleteDMixin


class OrderUser(UpdateDeleteDMixin, admin.ModelAdmin):
    """
    Класс OrderUser для изменения отображения
    модели Order в пользовательском интерфейсе админ-панели.
    """
    my_model = 'заказа'
    changer = 'app_order_order'
    list_display = [
        'id',
        'city',
        'user',
        'address',
        'get_payment_method_display',
        'order_number',
        'status',
        'commentary',
        'sum_order',
        'error_text',
        'get_delivery_method_display',
        'update_obj',
        'delete_obj',
    ]

    list_filter = ['id', 'user', 'payment_method', 'status']


admin.site.register(Order, OrderUser)
