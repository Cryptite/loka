from django.contrib.auth.models import User
from rest_framework import serializers
from loka.models import Town, Player, ArenaMatch

__author__ = 'tmiller'


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
    valleyScore = serializers.IntegerField()
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
            instance.name = attrs.get('name')
            instance.arenarating = attrs.get('arenarating')
            instance.arenawins = attrs.get('arenawins')
            instance.arenalosses = attrs.get('arenalosses')
            instance.streak = attrs.get('streak')
            instance.highestrating = attrs.get('highestrating')
            instance.arenarating2v2 = attrs.get('arenarating2v2')
            instance.arenawins2v2 = attrs.get('arenawins2v2')
            instance.arenalosses2v2 = attrs.get('arenalosses2v2')
            instance.streak2v2 = attrs.get('streak2v2')
            instance.highestrating2v2 = attrs.get('highestrating2v2')
            instance.valleyKills = attrs.get('valleyKills')
            instance.valleyDeaths = attrs.get('valleyDeaths')
            instance.valleyCaps = attrs.get('valleyCaps')
            instance.valleyWins = attrs.get('valleyWins')
            instance.valleyLosses = attrs.get('valleyLosses')
            instance.valleyScore = attrs.get('valleyScore')
            instance.title = attrs.get('title')
            instance.rank = attrs.get('rank')
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


class TownSerializer(serializers.HyperlinkedModelSerializer):
    name = serializers.CharField(max_length=50)
    motd = serializers.CharField(max_length=255, required=False)
    owner = serializers.CharField(max_length=50)
    subowners = serializers.CharField(required=False)
    members = serializers.CharField()

    def restore_object(self, attrs, instance=None):
        """
        Create or update a new snippet instance, given a dictionary
        of deserialized field values.

        Note that if we don't define this method, then deserializing
        data will simply return a dictionary of items.
        """
        print attrs
        if instance:
            # Update existing instance
            print 'Via existing instance'
            instance.name = attrs.get('name', instance.name)
            instance.motd = attrs.get('motd')
            instance.owner = self.resolve_owner(attrs.get("owner"))
            return instance

        owner = attrs.get("owner")
        del attrs["owner"]
        del attrs["members"]
        del attrs["subowners"]

        town = Town(**attrs)
        town.owner = self.resolve_owner(owner)
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


class ArenaMatchSerializer(serializers.HyperlinkedModelSerializer):
    pk = serializers.Field()
    date = serializers.DateTimeField()
    loser = serializers.CharField(max_length=50)
    winner = serializers.CharField(max_length=50)
    loser_rating = serializers.IntegerField()
    winner_rating = serializers.IntegerField()
    rating_change = serializers.IntegerField()
    loser_damage = serializers.IntegerField()
    winner_damage = serializers.IntegerField()
    length = serializers.IntegerField()

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
            instance.date = attrs.get('date', instance.date)
            instance.loser = attrs.get('loser', instance.loser)
            instance.winner = attrs.get('winner', instance.winner)
            instance.loser_rating = attrs.get('loser_rating', instance.loser_rating)
            instance.winner_rating = attrs.get('winner_rating', instance.winner_rating)
            instance.rating_change = attrs.get('rating_change', instance.rating_change)
            instance.loser_damage = attrs.get('loser_damage', instance.loser_damage)
            instance.winner_damage = attrs.get('winner_damage', instance.winner_damage)
            instance.length = attrs.get('length', instance.length)
            return instance

        # Create new instance
        return ArenaMatch(**attrs)

    class Meta:
        model = ArenaMatch
        fields = ('username', 'password', 'email')
        lookup_field = "username"