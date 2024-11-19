import random

from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.db.models import Prefetch
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse, reverse_lazy

from app_order.forms import OrderForm, Payment
from app_order.models import Order, ProductOrder
from app_order.services import create_order
from app_shop.cart import Cart
from app_shop.models import Product


def order_create(request: HttpRequest) -> HttpResponse:
    if request.method == "POST":
        form = OrderForm(request.POST or None)
        if form.is_valid():
            result = create_order(request, form.cleaned_data)
            if form.cleaned_data.get("pay") == "online":
                return redirect(reverse("payment", args=[result]))
            return redirect(reverse("payment_someone", args=[result]))
    form = OrderForm()
    cart = Cart(request)
    common_price = cart.common_price
    form_auth = AuthenticationForm()
    return render(
        request=request,
        template_name="app_order/order.html",
        context={
            "form": form,
            "cart": cart,
            "common_price": common_price,
            "form_auth": form_auth,
        },
    )


def payment_order(request: HttpRequest, order_number: int) -> HttpResponse:
    form = Payment(request.POST or None)
    if form.is_valid():
        card_number = form.cleaned_data.get("card_number")
        request.session["card_number"] = card_number
        return redirect(reverse("progress_payment", args=[order_number]))
    return render(
        request=request,
        template_name="app_order/payment.html",
        context={"form": form},
    )


def payment_someone_order(request: HttpRequest, order_number: int) -> HttpResponse:
    """Функция представление обработки формы случайного номера счета."""
    random_number = request.session.get("random_number")
    form = Payment(initial={"card_number": random_number})
    if request.method == "POST":
        form = Payment(request.POST)
        if form.is_valid():
            card_number = form.cleaned_data.get("card_number")
            request.session["card_number"] = card_number
            return redirect(reverse("progress_payment", args=[order_number]))
    return render(
        request=request,
        template_name="app_order/payment_someone.html",
        context={"form": form},
    )


def invoice_generator(request: HttpRequest) -> HttpResponse:
    """Функция представление генерации случайного числа."""
    generator = random.randint(10000000, 99999999)
    request.session["random_number"] = generator
    return redirect(request.META.get("HTTP_REFERER"))


@login_required(login_url=reverse_lazy("login_user"))
def history_order(request: HttpRequest) -> HttpResponse:
    orders = Order.objects.only(
        "delivery_method",
        "payment_method",
        "sum_order",
        "status",
        "order_number",
        "date_order",
    )
    return render(
        request=request,
        template_name="app_order/history_order.html",
        context={"orders": orders},
    )


@login_required(login_url=reverse_lazy("login_user"))
def one_order(request: HttpRequest, order_id: int) -> HttpResponse:
    order = get_object_or_404(
        Order.objects.select_related("user__profiles"), pk=order_id
    )
    products = ProductOrder.objects.prefetch_related(
        Prefetch("product", Product.objects.all())
    ).filter(order=order)
    return render(
        request=request,
        template_name="app_order/one_order.html",
        context={"order": order, "products": products},
    )
