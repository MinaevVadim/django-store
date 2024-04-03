from django import forms


def image_size(value):
    """
    Валидатор для контроля размера изображения
    при загрузке на сайт.
    """
    limit = 2 * 1024 * 1024
    if value.size > limit:
        raise forms.ValidationError(
            'Файл изображения можно '
            'использовать только размера не более 2 Мб.')
