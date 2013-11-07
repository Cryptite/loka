from django.contrib import admin

__author__ = 'tmiller'


class QuoteAdmin(admin.ModelAdmin):
    fields = ('text', 'author', 'event', 'event_url')