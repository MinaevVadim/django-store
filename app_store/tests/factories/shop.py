import io
import random

import factory
from faker import Factory as FakerFactory

from app_shop.models import Product, Category, Tag

faker = FakerFactory.create()


class CategoryFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Category

    name = factory.sequence(lambda x: "category%d" % x)
    active_category = factory.Faker("random_element", elements=["1", "2"])
    file_icon = factory.django.FileField(
        from_func=lambda: io.BytesIO(
            factory.Faker("binary").evaluate(None, None, {"locale": "en-us"})
        )
    )


class TagFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Tag

    name = factory.sequence(lambda x: "Tag%d" % x)


class ProductFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Product

    name = factory.sequence(lambda x: "product%d" % x)
    description = factory.Faker("sentence", nb_words=10)
    price = factory.sequence(lambda x: round(random.randint(1000, 9999), 2))
    limited_edition = factory.sequence(lambda x: random.choice([True, False]))
    count_goods = factory.Faker("random_number")
    active_product = factory.sequence(lambda x: random.choice([True, False]))

    @factory.post_generation
    def tags(self, create, extracted, **kwargs):
        if not create or not extracted:
            return
        rand = random.choice(extracted)
        self.tags.add(rand)

    category = factory.SubFactory(CategoryFactory)
