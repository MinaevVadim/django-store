import django_filters
from django import forms

from app_shop.models import Product, Tag, Category


class MyFilter(django_filters.FilterSet):
    price_up = django_filters.NumberFilter(
        label='цена от',
        method='filter_price_up',
    )
    price_from = django_filters.NumberFilter(
        label='цена до',
        method='filter_price_from'
    )
    name = django_filters.CharFilter(
        method='filter_name'
    )
    count_goods = django_filters.BooleanFilter(
        widget=forms.CheckboxInput,
        label='Только товары в наличии',
        method='filter_count_goods',
    )
    free_delivery = django_filters.BooleanFilter(
        widget=forms.CheckboxInput,
        label='С бесплатной доставкой',
        method='filter_free_delivery',
    )

    class Meta:
        model = Product
        fields = ['price_up', 'price_from', 'name', 'count_goods', 'free_delivery']

    @property
    def qs(self):
        queryset = super().qs
        data = self.__dict__['data']
        if data.get('novelty'):
            if data.get('novelty') == 'True':
                queryset = queryset.order_by('-date_product')
            else:
                queryset = queryset.order_by('date_product')
        if data.get('order_popular'):
            if data.get('order_popular') == 'True':
                queryset = queryset.order_by('-number_of_purchases')
            else:
                queryset = queryset.order_by('number_of_purchases')
        if data.get('order_price'):
            if data.get('order_price') == 'True':
                queryset = queryset.order_by('-price')
            else:
                queryset = queryset.order_by('price')
        if data.get('order_reviews'):
            if data.get('order_reviews') == 'True':
                queryset = queryset.order_by('-count_reviews')
            else:
                queryset = queryset.order_by('count_reviews')
        if data.get('tags'):
            queryset = queryset.filter(tags=Tag.objects.get(name=data.get('tags')))
        if data.get('category'):
            queryset = queryset.filter(category=Category.objects.get(name=data.get('category')))
        return queryset

    @classmethod
    def filter_price_up(cls, queryset, name, value):
        return queryset.filter(price__gte=value)

    @classmethod
    def filter_price_from(cls, queryset, name, value):
        return queryset.filter(price__lte=value)

    @classmethod
    def filter_name(cls, queryset, name, value):
        return queryset.filter(name=value)

    @classmethod
    def filter_count_goods(cls, queryset, name, value):
        if value:
            return queryset.filter(count_goods__gte=1)
        return queryset

    @classmethod
    def filter_free_delivery(cls, queryset, name, value):
        return queryset.filter(free_delivery=value)
