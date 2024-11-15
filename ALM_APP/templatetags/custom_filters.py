# yourapp/templatetags/custom_filters.py

from django import template

register = template.Library()

@register.filter
def get_item(list_data, index):
    try:
        return list_data[index]
    except IndexError:
        return None
    
    from django import template

@register.filter
def lookup(dict_data, key):
    try:
        # Ensure dict_data is a dictionary before attempting to access it
        if isinstance(dict_data, dict):
            return dict_data.get(key, "0.00")
        else:
            return "0.00"
    except Exception:
        return "0.00"
    
# @register.filter
# def lookup(dictionary, key):
#     return dictionary.get(key, "")

