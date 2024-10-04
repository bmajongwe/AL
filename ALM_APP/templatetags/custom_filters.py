# yourapp/templatetags/custom_filters.py

from django import template

register = template.Library()

@register.filter
def get_item(list_data, index):
    try:
        return list_data[index]
    except IndexError:
        return None
