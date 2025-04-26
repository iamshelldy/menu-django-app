from django import template

from menu.models import MenuItem


register = template.Library()


@register.inclusion_tag('menu/draw_menu.html', takes_context=True)
def draw_menu(context, menu_name: str):
    path = context['request'].path

    items = MenuItem.objects.filter(menu__name=menu_name).select_related('parent')

    active_item = find_active_item(items, path)

    open_items = build_open_items(active_item) if active_item else set()

    return {
        'menu_items': items,
        'open_items': open_items,
    }


def find_active_item(menu_items, path):
    for item in menu_items:
        if path.strip('/') == item.get_item_url().strip('/'):
            return item
    return None


def build_open_items(active_item):
    open_items = set()
    current = active_item
    while current:
        open_items.add(current.id)
        current = current.parent
    return open_items
