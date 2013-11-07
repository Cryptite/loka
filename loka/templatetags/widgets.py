from django import template
from loka.models import Quote, Player

__author__ = 'tmiller'

register = template.Library()

#@register.inclusion_tag("quote.html")
def get_quote():
    quotes = Quote.objects.order_by('?')
    if len(quotes) > 0:
        return {'quote': Quote.objects.order_by('?')[0]}
    return {'quote': []}

@register.assignment_tag
def player_avatar(user):
    player = Player.objects.get(name=user.username)
    return player.avatar

#register.assignment_tag(player_avatar)
register.inclusion_tag('quote.html')(get_quote)