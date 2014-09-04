from django.conf.urls import patterns, url, include
from django.contrib import admin
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from rest_framework import viewsets, routers

from loka import views
from loka.models import Town
from sitemap import LokaSitemap


admin.autodiscover()


# # ViewSets define the view behavior.
class TownViewSet(viewsets.ModelViewSet):
    model = Town


sitemaps = {
    'static': LokaSitemap,
}

# Routers provide an easy way of automatically determining the URL conf
router = routers.DefaultRouter()
router.register(r'town', TownViewSet)

urlpatterns = patterns('',
                       # Examples:
                       # url(r'^$', 'loka.views.home', name='home'),
                       # url(r'^loka/', include('loka.foo.urls')),

                       # Uncomment the admin/doc line below to enable admin documentation:
                       # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

                       # Uncomment the next line to enable the admin:
                       url(r'^admin/', include(admin.site.urls)),
                       url(r'^api/town', include(router.urls)),
                       url(r'^api/town/(?P<name>\w+)/$', views.TownDetail.as_view()),
                       url(r'^api/territory/(?P<name>\w+)/$', views.TerritoryDetail.as_view()),
                       url(r'^api/alliance/(?P<name>\w+)/$', views.AllianceDetail.as_view()),
                       url(r'^api/user/(?P<username>\w+)/$', views.UserDetail.as_view()),
                       url(r'^api/player/(?P<name>\w+)/$', views.PlayerDetail.as_view()),
                       url(r'^api/arenamatch', views.ArenaMatchDetail.as_view()),
                       url(r'^api/player_achievements/(?P<name>\w+)/$', views.PlayerAchievementsDetail.as_view()),
                       url(r'^api/achievement/(?P<name>\w+)/$', views.AchievementDetail.as_view()),
                       url(r'^api/search/', 'loka.views.search', name='search'),
                       url(r'^$', 'loka.views.home'),
                       url(r'^townslist', 'loka.views.townslist'),
                       url(r'^avatar/(?P<player_name>\w+)', 'loka.views.get_avatar'),
                       url(r'^getquote', 'loka.views.getquote'),
                       url(r'^about', 'loka.views.about'),
                       url(r'^donate', 'loka.views.donate'),
                       url(r'^thankyou', 'loka.views.thankyou'),
                       url(r'^towns', 'loka.views.towns'),
                       url(r'^pvpvota', 'loka.views.pvpvota'),
                       url(r'^pvpoverload', 'loka.views.pvpoverload'),
                       url(r'^pvp2v2', 'loka.views.pvp2v2'),
                       url(r'^pvp1v1', 'loka.views.pvp1v1'),
                       url(r'^pvp', 'loka.views.pvp'),
                       url(r'^map', 'loka.views.map_page'),
                       url(r'^deleteitem/(?P<item_id>\d+)', 'loka.views.deleteitem'),
                       url(r'^player/(?P<player_name>\w+)/achievements/(?P<category>\w+)',
                           'loka.views.player_achievements'),
                       url(r'^player/(?P<player_name>\w+)', 'loka.views.player'),
                       url(r'^issue/(?P<issue_id>\d+)', 'loka.views.issue'),
                       url(r'^issues', 'loka.views.issuelist'),
                       url(r'^town/(?P<town_name>\w+)/thread/(?P<thread_id>\d+)', 'loka.views.townthread'),
                       url(r'^town/(?P<town_name>\w+)/gallery', 'loka.views.towngallery'),
                       url(r'^town/(?P<town_name>\w+)/forum', 'loka.views.townforum'),
                       url(r'^town/(?P<town_name>\w+)', 'loka.views.townhome'),
                       url(r'^register/(?P<registration_id>\w+)', 'loka.views.registration'),
                       url(r'^logout', 'loka.views.logout'),
                       url(r'start$', 'loka.views.start', name="start"),
                       #url(r'ajax-upload$', views.import_uploader, name="my_ajax_upload"),
                       (r'^tinymce/', include('tinymce.urls')),
                       url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
                       (r'^sitemap\.xml$', 'django.contrib.sitemaps.views.sitemap', {'sitemaps': sitemaps})

)

urlpatterns += staticfiles_urlpatterns()