from django.urls import path

from app_payment.views import progress_payment

urlpatterns = [
    path('progress_payment/<int:order_number>', progress_payment, name='progress_payment'),
]
