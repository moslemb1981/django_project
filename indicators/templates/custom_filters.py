from django import template
register = template.Library()

@register.filter
def get_item(dictionary, key):
    """دسترسی به مقدار دیکشنری در قالب"""
    if dictionary and key in dictionary:
        return dictionary.get(key)
    return ""
