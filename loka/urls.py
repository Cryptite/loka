from django.conf.urls import patterns, url, include

from django.contrib import admin
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from rest_framework import viewsets, routers
from loka import views
from loka.models import Town

admin.autodiscover()


## ViewSets define the view behavior.
class TownViewSet(viewsets.ModelViewSet):
    model = Town

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
                       url(r'^townapi', include(router.urls)),
                       url(r'^townapi/(?P<pk>[0-9]+)/$', views.TownDetail.as_view()),
                       url(r'^$', 'loka.views.home'),
                       url(r'^townslist', 'loka.views.townslist'),
                       url(r'^avatar/(?P<player_name>\w+)', 'loka.views.getavatar'),
                       url(r'^getquote', 'loka.views.getquote'),
                       url(r'^about', 'loka.views.about'),
                       url(r'^towns', 'loka.views.towns'),
                       url(r'^pvp1v1', 'loka.views.pvp1v1'),
                       url(r'^pvp', 'loka.views.pvp'),
                       url(r'^deleteitem/(?P<item_id>\d+)', 'loka.views.deleteitem'),
                       url(r'^player/(?P<player_name>\w+)', 'loka.views.player'),
                       url(r'^town/(?P<town_name>\w+)/thread/(?P<thread_id>\d+)', 'loka.views.townthread'),
                       url(r'^town/(?P<town_name>\w+)/board', 'loka.views.townboard'),
                       url(r'^town/(?P<town_name>\w+)', 'loka.views.townhome'),
                       url(r'^register/(?P<registration_id>\w+)', 'loka.views.registration'),
                       url(r'^logout', 'loka.views.logout'),
                       url(r'start$', 'loka.views.start', name="start"),
                       #url(r'ajax-upload$', views.import_uploader, name="my_ajax_upload"),
                       url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
)

urlpatterns += staticfiles_urlpatterns()