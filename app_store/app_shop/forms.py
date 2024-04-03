from django import forms

from .models import Comment


class UserComment(forms.ModelForm):
    """Форма комментариев."""

    class Meta:
        model = Comment
        fields = ['name_user', 'text_comment']


class CountProductCart(forms.Form):
    """Форма выбора количества товара."""

    PRODUCT_CHOICES = [(i, str(i)) for i in range(1, 11)]

    count_good_basket = forms.TypedChoiceField(
        label='Количество',
        choices=PRODUCT_CHOICES,
        coerce=int,
    )
