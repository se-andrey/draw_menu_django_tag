from django.http import Http404
from django.views.generic.base import TemplateView

from common.views import TitleMixin
from menus.models import MenuItem


class IndexView(TitleMixin, TemplateView):
    template_name = 'menus/index.html'
    title = 'Главная'


class MenuView(TitleMixin, TemplateView):
    template_name = 'menus/menu.html'
    title = 'Меню'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        url = kwargs.get('url')
        menu_items = MenuItem.objects.filter(url=url)
        if not menu_items.exists():
            raise Http404()
        context['menu_items'] = menu_items
        context['url'] = url
        return context
