# filters.py
from django import template

register = template.Library()

@register.filter()
def times(number):
    return range(number)

@register.filter
def gender_label(value):
    gender_map = {
        'M': 'Male',
        'F': 'Female',
        'O': 'Other',
    }
    return gender_map.get(value, 'None')