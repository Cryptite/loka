from django.contrib.auth.models import User
from rest_framework import serializers
from loka.models import Town, Player

__author__ = 'tmiller'


class TownSerializer(serializers.HyperlinkedModelSerializer):
    name = serializers.CharField(max_length=50)
    motd = serializers.CharField(max_length=255, required=False)
    owner = serializers.CharField(max_length=50)
    subowners = serializers.CharField(max_length=100, required=False)
    members = serializers.CharField(max_length=1000)

    def restore_object(self, attrs, instance=None):
        """
        Create or update a new snippet instance, given a dictionary
        of deserialized field values.

        Note that if we don't define this method, then deserializing
        data will simply return a dictionary of items.
        """

        if instance:
            # Update existing instance
            print 'Via existing instance'
            instance.name = attrs.get('name', instance.name)
            instance.motd = attrs.get('motd', instance.motd)
            instance.owner = self.resolve_owner(attrs.get('owner'))
            instance.set_many_field(attrs.get("subowners"), instance.subowners)
            instance.set_many_field(attrs.get("members"), instance.members)
            return instance

        # Create new instance
        town = Town.objects.create(name=attrs.get("name"),
                                   motd=attrs.get("motd"),
                                   owner=self.resolve_owner(attrs.get("owner")))
        town.set_many_field(attrs.get("subowners"), town.subowners)
        town.set_many_field(attrs.get("members"), town.members)
        # return town

    def save(self, **kwargs):
        print 'SAVE',kwargs
        return super(TownSerializer, self).save(**kwargs)

    def save_object(self, obj, **kwargs):
        print 'SAVE_OBJECT',obj,kwargs
        super(TownSerializer, self).save_object(obj, **kwargs)


    def resolve_owner(self, owner_name):
        print "Resolving owner: ", owner_name
        owner = Player.objects.filter(name=owner_name)
        if not owner:
            return Player.objects.create(name=owner_name)
        else:
            return owner[0]

    class Meta:
        model = Town
        fields = ('name', "motd", "owner", "subowners", "members")
        lookup_field = "name"


class UserSerializer(serializers.HyperlinkedModelSerializer):
    pk = serializers.Field()
    username = serializers.CharField(max_length=50)
    password = serializers.CharField(max_length=20)
    email = serializers.EmailField()

    def restore_object(self, attrs, instance=None):
        """
        Create or update a new snippet instance, given a dictionary
        of deserialized field values.

        Note that if we don't define this method, then deserializing
        data will simply return a dictionary of items.
        """
        if instance:
            # Update existing instance
            print 'Via existing instance'
            instance.username = attrs.get('name', instance.username)
            instance.password = attrs.get('password', instance.password)
            instance.email = attrs.get('email', instance.email)
            return instance

        # Create new instance
        return User(**attrs)

    class Meta:
        model = User
        fields = ('username', 'password', 'email')
        lookup_field = "username"