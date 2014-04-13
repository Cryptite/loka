from django import template

from loka.models import Player, UnlockedAchievement, Achievement


__author__ = 'tmiller'

register = template.Library()


@register.simple_tag
def get_earned_achievements_by_category(player, category):
    return UnlockedAchievement.objects.filter(player=Player.objects.get(name=player),
                                              achievement__category=category).order_by("date")


@register.simple_tag
def get_earned_number_achievements_by_category(player, category):
    return get_earned_achievements_by_category(player, category).count()


@register.simple_tag
def get_all_achievements_by_category(category):
    return Achievement.objects.filter(category=category)


@register.simple_tag
def get_achievement_percentage_by_category(player, category):
    return int((float(get_earned_achievements_by_category(player, category).count()) / float(
        get_all_achievements_by_category(category).count())) * 100.0)


@register.simple_tag
def get_achievement_string_by_category(player, category):
    return "{}/{} {}%".format(get_earned_achievements_by_category(player, category).count(),
                              get_all_achievements_by_category(category).count(),
                              get_achievement_percentage_by_category(player, category))