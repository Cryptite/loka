from django.conf.urls import patterns, url

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()
from django.views.generic import TemplateView

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'loka.views.home', name='home'),
    # url(r'^loka/', include('loka.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # url(r'^admin/', include(admin.site.urls)),

    url(r'^$', 'loka.views.home'),
    url(r'^townslist', 'loka.views.townslist'),
    url(r'^towns', 'loka.views.towns'),
    url(r'^pvp1v1', 'loka.views.pvp1v1'),
    url(r'^pvp', 'loka.views.pvp'),
    url(r'^player/(?P<player_name>\w+)', 'loka.views.player'),
    url(r'^register/(?P<registration_id>\w+)', 'loka.views.registration'),
    #url(r'^form_inline$', 'loka.views.demo_form_inline'),
    #url(r'^formset$', 'loka.views.demo_formset', {}, "formset"),
    #url(r'^tabs$', 'loka.views.demo_tabs', {}, "tabs"),
    #url(r'^pagination$', 'loka.views.demo_pagination', {}, "pagination"),
    #url(r'^widgets$', 'loka.views.demo_widgets', {}, "widgets"),
    #url(r'^buttons$', TemplateView.as_view(template_name='buttons.html'), name="buttons"),
)
