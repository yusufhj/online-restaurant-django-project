from django import template

register = template.Library()

# customer filer to handle displaying order quantity in order details page
@register.filter
def hash(passed_dict, key):
    return passed_dict.get(key)