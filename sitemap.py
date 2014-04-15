from django.contrib.sitemaps import Sitemap
from django.core.urlresolvers import reverse

__author__ = 'Tom'


class LokaSitemap(Sitemap):
    priority = 0.5
    changefreq = "weekly"

    def items(self):
        return ['loka.views.home', 'loka.views.towns', 'loka.views.pvp', 'loka.views.townslist', 'loka.views.pvp1v1',
                'loka.views.pvp2v2', 'loka.views.pvpvota', 'loka.views.pvpoverload']

    def location(self, obj):
        return reverse(obj)
