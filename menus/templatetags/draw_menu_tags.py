from django import template
from django.urls import resolve, reverse
from django.utils.safestring import mark_safe

from menus.models import MenuItem

register = template.Library()


@register.simple_tag(takes_context=True)
def draw_menu(context, menu_name):
    """
    Тег draw_menu позволяет формировать древовидное меню на странице
    :param context:
    :param menu_name: имя меню в таблице
    :return:
    """
    current_url = context['request'].path
    resolved_url = resolve(current_url)
    menu_items = MenuItem.objects.filter(menu_name=menu_name).select_related('parent')

    # Собираем словарь с элементами меню
    menu_items_dict = {}
    for item in menu_items:
        menu_items_dict[item.id] = {
            'item': item,
            'parent_id': [item.parent_id],
            'children': [],
            'active': item.url == resolved_url.kwargs['url'],
            'url': item.url
        }

    # Определяем текущий пункт меню, всех детей для каждого пункта меню. Путь от активного пукнта меню до верхнего
    for item_id, item_data in menu_items_dict.items():
        parent_id = item_data['parent_id']
        # Заполняем children
        if parent_id[-1] is not None:
            for menu_id in menu_items_dict:
                if parent_id[-1] == menu_id:
                    menu_items_dict[parent_id[-1]]['children'].append(item_id)

        # Для активного пункта меню определяем всех родителей
        if item_data['active']:
            if parent_id[-1] is not None:
                parent_id = menu_items_dict[parent_id[-1]]['parent_id']
                while parent_id[-1] is not None:
                    menu_items_dict[item_id]['parent_id'].extend(parent_id)
                    parent_id = menu_items_dict[parent_id[-1]]['parent_id']

    # Строим меню
    menu_html = build_menu(menu_items_dict)

    # Возвращаем через mark_safe для построения html кода
    return mark_safe(menu_html)


def build_menu(menu_items_dict, node=None, target=None, visited=None, level=1):
    """
    Строит древовидное меню на основе переданного словаря, который содержит информацию о пунктах меню.
    Меню раскрыто до текущего пункта, плюс раскрыто на один дочерний уровень, если он есть.
    Основана на DFS (алгоритме поиска в глубину)

    :param menu_items_dict: словарь вида {id: {'item': 'пункт меню', 'parent_id': [4], 'children': [6], 'active': True}
    active - текущий пункт меню
    :param node: список элементов вида [id, 'html код для пукнта меню']
    :param target: список, содержащий активный (текущий) пукнт меню, вида [id, 'html код для пукнта меню']
    :param visited: список посещенных пукнтов меню
    :param level: уровень глубины рекурсии, используется для формирования отступов и правильного закрытия тегов </ul>
    :return: возвращает строку с HTML кодом построенного меню с правильными отступами
    """
    # Определяем главный пункт меню
    if node is None:
        for id, item in menu_items_dict.items():
            if item.get('parent_id')[-1] is None:
                node = [id, item.get("item")]
                break

    # Если родителя нет, выйдем из функции
    if node is None:
        return

    # Определяем выбранный пукнт меню
    if target is None:
        for id, item in menu_items_dict.items():
            if item.get('active'):
                target = [id, item.get('item')]
                break

    # Если активного пункта меню нет, то вернет только родительский пукнт меню
    if target is None:
        url = reverse('menus:menu_view', args=[menu_items_dict[node[0]].get('url')])
        return f'<ul>\n        <li><a href="{url}">{node[1]}</a></li>\n    </ul>'

    # При первом закуске инициализируем пустой спискок посещенный нод (пунктов меню)
    if visited is None:
        visited = []

    # Определяем url для текущей ноды
    url = reverse('menus:menu_view', args=[menu_items_dict[node[0]].get('url')])

    # Формируем пункт меню для ноды
    node[1] = f'{"    " * (level)}<li><a href="{url}">{node[1]}</a></li>\n'

    # Проверяем есть ли дочерние пункты меню у текущего. Если есть, то открываем <ul>
    if menu_items_dict[node[0]].get('children'):
        node[1] += f'{"    " * (level + 1)}<ul>\n'

    # добавляем ноду в список посещенных
    visited.append(node)

    # Если текущий пункт меню равен выбранному, то добавляем его ближайших детей и выходим из рекурсии
    if node[0] == target[0]:
        children = menu_items_dict[node[0]].get('children')
        if children:
            for child in children:
                url = reverse('menus:menu_view', args=[menu_items_dict[child].get('url')])
                child_item = f'{"    " * (level + 1)}<li><a href="{url}">' \
                             f'{menu_items_dict[child].get("item")}</a></li>\n'
                visited.append([child, child_item])
            visited.append(['active', f'{"    " * (level + 1)}</ul>\n'])

        # Закрываем теги <ul>, их количество определяется глубиной рекурсии
        for indent in range(level, 1, -1):
            visited.append(['active', f'{"    " * (indent)}</ul>\n'])

        # возвращаем готовых html код меню
        return '<ul>\n' + ''.join([html[1] for html in visited]) + '    </ul>\n'

    # Определяем дочерние пункты меню
    child_menu = menu_items_dict[node[0]]['children']
    if child_menu:
        for child_menu_item in child_menu:

            # Формируем ноду
            child_menu_item_full = [child_menu_item, menu_items_dict[child_menu_item]['item']]

            # Формируем список из id поседенных нод
            visited_menus = [num_node[0] for num_node in visited]

            # Если еще не посещали пункт меню, то вызовем себя
            if child_menu_item_full[0] not in visited_menus:
                path = build_menu(menu_items_dict, child_menu_item_full, target, visited, level + 1)

                # Закроем тег <ul> если у данного пукнта меню были дочерние
                if menu_items_dict[child_menu_item_full[0]].get('children'):
                    visited.append(['close ul', f'{"    " * (level + 2)}</ul>\n'])
                if path:
                    return path
