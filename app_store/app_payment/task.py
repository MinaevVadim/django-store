import datetime

from django.shortcuts import get_object_or_404

from app_order.models import Order, ProductOrder
from store.celery import app


@app.task
def job(order_number: int, card_number: str) -> bool | str:
    order_confirmation = get_object_or_404(Order, order_number=order_number)
    check_payment = int(card_number) % 2 == 0 and not str(card_number).endswith('0')
    if check_payment:
        order_confirmation.status = 'False'
        order_confirmation.error_text = 'Хороший покупатель!'
        order = ProductOrder.objects.filter(order=order_confirmation)
        for i in order:
            i.product.count_goods -= i.count
            i.product.save()
        order_confirmation.save()
        return f'Заказ № {order_number} был оплачен {datetime.datetime.now()}'
    else:
        order_confirmation.error_text = 'Плохой покупатель'
        order_confirmation.save()
        return False
