from django import template
from loka.models import Quote

__author__ = 'tmiller'

register = template.Library()

@register.inclusion_tag("quote.html")
def get_quote():
    return {'quote': Quote.objects.order_by('?')[0]}

register.inclusion_tag('quote.html')(get_quote)