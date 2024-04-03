from django.http import HttpRequest

from app_shop.cart import Cart
from app_shop.models import Category


def social(request: HttpRequest) -> dict:
    """
    Функция для отображения категорий товаров
    и общей суммы товаров в карзине.
    """
    categories = Category.objects.only('name', 'file_icon', 'level')
    cart = Cart(request)
    return {
        'categories': categories,
        'count_cart': len(cart),
        'common_price': cart.common_price,
    }
