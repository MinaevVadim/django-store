from django.urls import path

from app_shop.views import MainList, ListShop, AboutSite, DetailProductList, load_more, cart_add_product, cart_user, \
    cart_remove

urlpatterns = [
    path('', MainList.as_view(), name='main'),
    path('catalog/', ListShop.as_view(), name='catalog'),
    path('about/', AboutSite.as_view(), name='about'),
    path('product/<int:pk>', DetailProductList.as_view(), name='product'),
    path('load_more', load_more, name='load_more'),
    path('cart/<int:product_id>', cart_add_product, name='cart'),
    path('cart/', cart_user, name='cart_user'),
    path('delete/<int:product_id>', cart_remove, name='cart_delete'),
]
