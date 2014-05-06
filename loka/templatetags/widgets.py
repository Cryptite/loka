from django import template

from loka.models import Quote, Player, TownMedia


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
    try:
        player = Player.objects.get(name=user.username)
        return player.avatar
    except Exception, e:
        return None


@register.filter
def has_town_banner(town):
    image = TownMedia.objects.filter(town__name=town)
    if image:
        print 'returning', image[0]
        return image[0]
    else:
        return None


@register.simple_tag
def get_town_banner(town):
    image = TownMedia.objects.filter(town__name=town)
    if image:
        return image[0]
    else:
        return None

#register.assignment_tag(player_avatar)
register.inclusion_tag('quote.html')(get_quote)