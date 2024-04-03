from decimal import Decimal
from typing import Iterator

from django.conf import settings
from django.http import HttpRequest

from app_shop.models import Product


class Cart:

    def __init__(self, request: HttpRequest) -> None:
        """
        Инициализируем корзину
        """
        self.session = request.session
        cart = self.session.get(settings.CART_SESSION_ID)
        if not cart:
            cart = self.session[settings.CART_SESSION_ID] = {}
        self.cart = cart

    def add(self, product: Product, quantity=1) -> None:
        """
        Добавить продукт в корзину или обновить его количество.
        """
        product_id = str(product.id)
        if product_id not in self.cart:
            self.cart[product_id] = {'quantity': 0,
                                     'price': str(product.price)}
        self.cart[product_id]['quantity'] = quantity
        self.save()

    @property
    def common_price(self) -> int:
        result = sum(
            [int(i['quantity']) * float(i['price']) for i in self.cart.values()]
        )
        return result

    def save(self) -> None:
        self.session[settings.CART_SESSION_ID] = self.cart
        self.session.modified = True

    def remove(self, product: Product) -> None:
        """
        Удаление товара из корзины.
        """
        product_id = str(product.id)
        if product_id in self.cart:
            del self.cart[product_id]
            self.save()

    def __iter__(self) -> Iterator:
        """
        Перебор элементов в корзине и получение продуктов из базы данных.
        """
        product_ids = self.cart.keys()
        products = Product.objects.filter(id__in=product_ids)
        for product in products:
            self.cart[str(product.id)]['product'] = product

        for item in self.cart.values():
            item['quantity'] = item['quantity']
            item['price'] = Decimal(item['price']) * item['quantity']
            yield item

    def __len__(self) -> int:
        """
        Подсчет всех товаров в корзине.
        """
        return sum(item['quantity'] for item in self.cart.values())

    def clear(self) -> None:
        """
        Удаление корзины из сессии
        """
        del self.session[settings.CART_SESSION_ID]
        self.session.modified = True
