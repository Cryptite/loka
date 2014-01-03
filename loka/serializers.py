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
            return instance

        owner = attrs.get("owner")
        subowners = attrs.get("subowners")
        members = attrs.get("members")
        del attrs["owner"]
        del attrs["subowners"]
        del attrs["members"]

        town = Town(**attrs)
        town.owner = self.resolve_owner(owner)
        town.set_many_field(members, town.members)
        town.set_many_field(subowners, town.subowners)
        return town

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


class PlayerSerializer(serializers.HyperlinkedModelSerializer):
    pk = serializers.Field()
    name = serializers.CharField(max_length=30)
    arenarating = serializers.IntegerField()
    arenawins = serializers.IntegerField()
    arenalosses = serializers.IntegerField()
    streak = serializers.IntegerField()
    highestrating = serializers.IntegerField()
    arenarating2v2 = serializers.IntegerField()
    arenawins2v2 = serializers.IntegerField()
    arenalosses2v2 = serializers.IntegerField()
    streak2v2 = serializers.IntegerField()
    highestrating2v2 = serializers.IntegerField()
    valleyKills = serializers.IntegerField()
    valleyDeaths = serializers.IntegerField()
    valleyCaps = serializers.IntegerField()
    valleyWins = serializers.IntegerField()
    valleyLosses = serializers.IntegerField()
    title = serializers.CharField(max_length=20, required=False)
    rank = serializers.CharField(max_length=20, required=False)

    def restore_object(self, attrs, instance=None):
        """
        Create or update a new snippet instance, given a dictionary
        of deserialized field values.

        Note that if we don't define this method, then deserializing
        data will simply return a dictionary of items.
        """
        if instance:
        #     Update existing instance
            print 'Via existing instance'
            instance.name = attrs.get('name', instance.name)
            # instance.password = attrs.get('password', instance.password)
            # instance.email = attrs.get('email', instance.email)
            return instance

        # Create new instance
        player = Player(**attrs)
        user_object = User.objects.filter(username=attrs.get("name"))
        if user_object:
            player.user = user_object[0]
        return Player(**attrs)

    class Meta:
        model = User
        fields = ('name', 'arenarating', 'arenawins', 'arenalosses', 'streak', 'highestrating',
                  'arenarating2v2', 'arenawins2v2', 'arenalosses2v2', 'streak2v2', 'highestrating2v2',
                  'valleyKills', 'valleyDeaths', 'valleyCaps', 'valleyWins', 'valleyLosses', 'title', 'rank')
        lookup_field = "name"