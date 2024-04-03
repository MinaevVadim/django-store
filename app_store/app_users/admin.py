from django.contrib import admin
from django.utils.safestring import mark_safe

from .models import Profile


class ProFileAdmin(admin.ModelAdmin):
    """
    Класс ProFileAdmin для изменения отображения
    модели Profile в пользовательском интерфейсе админ-панели.
    """

    list_display = ['id', 'number', 'user', 'get_html_image_avatar']
    list_filter = ['id', 'user']

    def get_html_image_avatar(self, obj):
        """Метод отображения изображения в виде кортинки."""
        if obj.image_avatar:
            return mark_safe(
                "<img src='{obj.image_avatar.url}' width=50>"
            )

    get_html_image_avatar.short_description = 'аватарка'


admin.site.register(Profile, ProFileAdmin)
