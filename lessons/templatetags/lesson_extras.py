from django import template


register = template.Library()


@register.filter
def get_item(mapping, key):
    """Позволяет в шаблоне получить значение словаря по ключу."""

    return mapping.get(key)
