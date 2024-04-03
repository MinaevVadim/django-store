from django.contrib.messages.views import SuccessMessageMixin
from django.core.cache import cache
from django.db.models import F
from django.http import JsonResponse, HttpResponseRedirect, HttpRequest, HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from django.views.generic import ListView, TemplateView, DetailView

from app_shop.cart import Cart
from app_shop.filters import MyFilter
from app_shop.forms import UserComment, CountProductCart
from app_shop.models import Product, Tag


class MainList(SuccessMessageMixin, ListView):
    """Класс представление получения списка товаров."""

    queryset = Product.objects.all()
    template_name = 'app_shop/index.html'
    success_message = 'Товар добавлен в корзину!'

    def get_context_data(self, *, object_list=None, **kwargs) -> dict:
        """
        Метод объединения данных контекста всех родительских
        классов с данными избранных, популярных
        и с ограниченным тиражом товаров.
        """
        context = super(MainList, self).get_context_data(
            object_list=None,
            **kwargs
        )
        context['populars'] = self.object_list[:9]
        context['favorites'] = self.object_list[:3]
        context['limited_edition'] = self.object_list.filter(
            limited_edition=True)[:32]
        return context


class ListShop(ListView):
    """
    Класс представление получения списка
    каталога с активными продуктами.
    """

    paginate_by = 6
    queryset = Product.objects.prefetch_related('category')
    template_name = 'app_shop/catalog.html'
    context_object_name = 'products'

    def get_context_data(self, *, object_list=None, **kwargs) -> dict:
        """
        Метод объединения данных контекста всех родительских
        классов с данными тегов и формой фильтрации.
        """
        context = super().get_context_data(**kwargs)
        context['tags'] = Tag.objects.all()
        context['filter'] = MyFilter(self.request.GET, self.queryset)
        return context


def cart_add_product(request: HttpRequest, product_id: int) -> HttpResponse:
    """
    Добавление товара в корзину
    """
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    form = CountProductCart(request.POST)
    if form.is_valid():
        values = form.cleaned_data
        cart.add(
            product=product,
            quantity=values['count_good_basket'],
        )
    return redirect(reverse('cart_user'))


def cart_user(request: HttpRequest) -> HttpResponse:
    """
    Корзина пользователя
    """
    cart = Cart(request)
    context = {
        'cart': cart,
        'common_price': cart.common_price,
    }
    return render(request, 'app_shop/cart.html', context=context)


def cart_remove(request: HttpRequest, product_id: int) -> HttpResponse:
    """
    Удаление корзины
    """
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    cart.remove(product)
    return redirect(reverse('cart_user'))


class AboutSite(TemplateView):
    """Функция представление информации о магазине."""
    template_name = 'app_shop/about.html'


class DetailProductList(DetailView):
    """
    Класс представление детальной информации
    о товаре и комментраиев к нему.
    """

    queryset = Product.objects.prefetch_related('product_comments')
    template_name = 'app_shop/product.html'

    def get_context_data(self, **kwargs) -> dict:
        """
        Метод объединения данных контекста всех
        родительских классов с данными комментариев о товаре,
        количества отзывов, формой комментариев,
        формой выбора количества продукта и тегов.
        """
        context = super().get_context_data(**kwargs)
        context['posts'] = self.object.product_comments.select_related('user__profiles')[0:3]
        context['form_comment'] = UserComment
        context['form_count_cart'] = CountProductCart
        context['tags'] = self.object.tags.all()
        context['count_reviews'] = self.object.product_comments.count()

        key_product = 'key_product_%s' % self.object.id
        cache_product = cache.get(key_product)
        if not cache_product:
            cache.set(key_product, self.object, 1440 * 60)

        return context

    def post(self, request: HttpRequest, *args, **kwargs) -> HttpResponse:
        """
        Метод получения данных формы комментария и их обработка.
        """
        comment_form = UserComment(request.POST)
        if comment_form.is_valid():
            reply = comment_form.save(commit=False)
            reply.product = self.get_object()
            reply.name_user = request.user.first_name
            reply.user = request.user
            reply.save()
            self.object = self.get_object()
            self.object.save()
            return HttpResponseRedirect(
                reverse('product', args=[self.object.id])
            )


def load_more(request: HttpRequest) -> HttpResponse:
    """
    Функция обработки запроса на отображение
    дополнительных комментариев.
    """
    offset = int(request.GET.get('loaded_item'))
    limit = 3
    product_all = get_object_or_404(Product).product_comments.all()
    posts = list(product_all.annotate(
        image_avatar=F('user__profiles__image_avatar')).values())[offset:limit + offset]
    return JsonResponse(data={'posts': posts})
