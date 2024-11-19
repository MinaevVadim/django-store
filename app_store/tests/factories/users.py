import factory
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password
from faker import Factory as FakerFactory

from app_shop.models import Comment
from app_users.models import Profile
from tests.factories.shop import ProductFactory

faker = FakerFactory.create()


class ProfileFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Profile


class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = User

    username = factory.Faker("name")
    password = factory.LazyFunction(lambda: make_password("qwerty"))
    first_name = factory.Faker("first_name")
    last_name = factory.Faker("last_name")

    profile = factory.RelatedFactory(ProfileFactory, "user")


class CommentFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Comment

    name_user = factory.Faker("name")
    text_comment = factory.Faker("sentence", nb_words=10)
    product = factory.SubFactory(ProductFactory)
    user = factory.SubFactory(UserFactory)
