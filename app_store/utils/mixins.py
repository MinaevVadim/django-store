from django.db.models import Model
from django.http import HttpResponse
from django.urls import reverse
from django.utils.html import format_html


class UpdateDeleteDMixin:
    """Миксин для редактирования и удаления объектов"""
    changer: str = ''
    my_model: str = ''

    def update_obj(self, obj: Model) -> HttpResponse:
        """Метод изменения объекта."""
        url = reverse(
            'admin:%s_change' % self.changer,
            args=[obj.id],
        )
        return format_html(
            '<a href="{}">редактирование</a>',
            url,
        )

    def delete_obj(self, obj: Model) -> HttpResponse:
        """Метод удаления объекта."""
        url = reverse('admin:%s_delete' % self.changer, args=[obj.id])
        return format_html('<a href="{}">удаление</a>', url)

    update_obj.short_description = 'изменение %s' % my_model
    delete_obj.short_description = 'удаление %s' % my_model
