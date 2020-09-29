import random
from django import template
register = template.Library()

# register = template.Library()


# @register.filter
# def random_int(a, b=None):
#     if b is None:
#         a, b = 0, a
#     return random.randint(a, b)


@register.filter
def multiply(value, arg):
    return value * arg
