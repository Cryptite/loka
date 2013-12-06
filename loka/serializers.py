from rest_framework import serializers
from loka.models import Town

__author__ = 'tmiller'


class TownSerializer(serializers.HyperlinkedModelSerializer):
    pk = serializers.Field()  # Note: `Field` is an untyped read-only field.
    name = serializers.CharField(max_length=50)
    tag = serializers.CharField(max_length=50)
    motd = serializers.CharField(max_length=255)

    def restore_object(self, attrs, instance=None):
        """
        Create or update a new snippet instance, given a dictionary
        of deserialized field values.

        Note that if we don't define this method, then deserializing
        data will simply return a dictionary of items.
        """
        if instance:
            # Update existing instance
            instance.name = attrs.get('name', instance.name)
            instance.tag = attrs.get('tag', instance.tag)
            instance.motd = attrs.get('motd', instance.motd)
            return instance

        # Create new instance
        return Town(**attrs)

    class Meta:
        model = Town
        fields = ('name', 'tag', 'motd')