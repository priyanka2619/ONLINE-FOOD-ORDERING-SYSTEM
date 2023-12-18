from django import template
from restaurant.models import MenuItem

register = template.Library()

@register.filter(name='currency')
def currency(number):
    return "₹ "+ str(number)