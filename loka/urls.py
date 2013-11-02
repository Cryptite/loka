from django.conf.urls import patterns, url, include

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
from django.contrib import admin
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from dajaxice.core import dajaxice_autodiscover, dajaxice_config

admin.autodiscover()
dajaxice_autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'loka.views.home', name='home'),
    # url(r'^loka/', include('loka.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),

    url(r'^$', 'loka.views.home'),
    url(r'^townslist', 'loka.views.townslist'),
    url(r'^towns', 'loka.views.towns'),
    url(r'^pvp1v1', 'loka.views.pvp1v1'),
    url(r'^pvp', 'loka.views.pvp'),
    url(r'^player/(?P<player_name>\w+)', 'loka.views.player'),
    url(r'^town/(?P<town_name>\w+)', 'loka.views.town'),
    url(r'^register/(?P<registration_id>\w+)', 'loka.views.registration'),
    url(r'^logout', 'loka.views.logout'),
    (dajaxice_config.dajaxice_url, include('dajaxice.urls')),
)

urlpatterns += staticfiles_urlpatterns()