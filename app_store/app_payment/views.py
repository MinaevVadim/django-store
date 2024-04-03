from django.http import HttpRequest, HttpResponse
from django.shortcuts import render
from app_payment.task import job


def progress_payment(request: HttpRequest, order_number: int) -> HttpResponse:
    job.delay(
        order_number,
        request.session.get('card_number'),
    )
    return render(
        request=request,
        template_name='app_payment/progressPayment.html',
    )
