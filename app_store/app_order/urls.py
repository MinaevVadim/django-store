from django.urls import path

from app_order.views import order_create, payment_order, payment_someone_order, history_order, one_order, \
    invoice_generator

urlpatterns = [
    path('order/', order_create, name='order'),
    path('payment/<int:order_number>', payment_order, name='payment'),
    path('payment_someone/<int:order_number>', payment_someone_order, name='payment_someone'),
    path('history_order/', history_order, name='history_order'),
    path('one_order/<int:order_id>', one_order, name='one_order'),
    path('invoice_generator/', invoice_generator, name='invoice_generator'),
]
