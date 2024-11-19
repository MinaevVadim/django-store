import random
from factory import fuzzy
import factory
from faker import Factory as FakerFactory

from app_order.models import (
    Order,
    ProductOrder,
    DELIVERY_METHOD,
    METHOD_PAYMENT,
    STATUS_PAYMENT,
)
from tests.factories.shop import ProductFactory
from tests.factories.users import UserFactory

faker = FakerFactory.create()


class OrderFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Order

    city = factory.Faker("city")
    commentary = factory.Faker("sentence", nb_words=10)
    error_text = factory.Faker("sentence", nb_words=10)
    address = factory.Faker("address")
    order_number = factory.Faker("random_number")
    sum_order = fuzzy.FuzzyDecimal(0, 10)
    payment_method = fuzzy.FuzzyChoice([x[0] for x in METHOD_PAYMENT])
    status = fuzzy.FuzzyChoice([x[0] for x in STATUS_PAYMENT])
    delivery_method = fuzzy.FuzzyChoice([x[0] for x in DELIVERY_METHOD])

    @factory.post_generation
    def products(self, create, extracted, **kwargs):
        if not create or not extracted:
            return
        rand = random.choice(extracted)
        self.products.add(rand)

    user = factory.SubFactory(UserFactory)


class ProductOrderFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = ProductOrder

    product = factory.SubFactory(ProductFactory)
    order = factory.SubFactory(OrderFactory)
    count = factory.Faker("random_number")
    price = fuzzy.FuzzyDecimal(0, 10)
