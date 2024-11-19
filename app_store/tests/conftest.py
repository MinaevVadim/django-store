import pytest
from pytest_factoryboy import register

from app_users.models import Profile
from tests.factories.orders import OrderFactory, ProductOrderFactory
from tests.factories.shop import CategoryFactory, TagFactory, ProductFactory
from tests.factories.users import UserFactory, CommentFactory, ProfileFactory

register(CategoryFactory)
register(TagFactory)
register(ProductFactory)
register(UserFactory)
register(CommentFactory)
register(OrderFactory)
register(ProductOrderFactory)
register(ProfileFactory)


@pytest.fixture
def auto_login_user(client, user_factory):
    def make_auto_login():
        user = user_factory.create()
        client.login(username=user.username, password="qwerty")
        return client, user

    return make_auto_login


@pytest.fixture
def create_order(user_factory, product_factory, order_factory, product_order_factory):
    user = user_factory.create()
    product = product_factory.create()
    order = order_factory.create(user=user)
    product_order_factory.create(order=order, product=product)
    return order, user, product


@pytest.fixture
def create_user_profile(user_factory):
    user = user_factory.create()
    profile = Profile.objects.get(user=user)
    return user, profile
