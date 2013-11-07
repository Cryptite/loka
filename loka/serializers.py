from rest_framework import serializers
from loka.models import Town

__author__ = 'tmiller'


class TownSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Town
        fields = ('name', 'tag', 'motd')