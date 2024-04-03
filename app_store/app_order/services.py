import random

from django.http import HttpRequest

from app_order.models import Order, ProductOrder
from app_shop.cart import Cart
from django.db import transaction


def generate_order_number() -> int:
    unique_number = True
    random_number = 0
    while unique_number:
        random_number = random.randint(1, 10000)
        unique_number = Order.objects.filter(
            order_number=random_number).exists()
    return random_number


@transaction.atomic
def create_order(request: HttpRequest, dict_values: dict) -> int:
    cart = Cart(request)
    new_order = Order.objects.create(
        user=request.user,
        delivery_method=dict_values.get('delivery'),
        city=dict_values.get('city'),
        address=dict_values.get('address'),
        payment_method=dict_values.get('pay'),
        order_number=generate_order_number(),
        sum_order=cart.common_price,
    )
    list_create = [
        ProductOrder(
            product=i.get('product'),
            order=new_order,
            count=i.get('quantity'),
            price=i.get('price')
        ) for i in cart]
    ProductOrder.objects.bulk_create(list_create)
    return new_order.order_number
