from django.contrib import admin
from django.contrib.auth.models import User
from django.db import models


# Create your models here.
def retrieve_avatar(self):
    pass


class Player(models.Model):
    name = models.CharField(max_length=30)
    arenarating = models.SmallIntegerField(blank=True, null=True)
    arenawins = models.SmallIntegerField(blank=True, null=True)
    arenalosses = models.SmallIntegerField(blank=True, null=True)
    streak = models.SmallIntegerField(blank=True, null=True)
    highestrating = models.SmallIntegerField(blank=True, null=True)
    arenarating2v2 = models.SmallIntegerField(blank=True, null=True)
    arenawins2v2 = models.SmallIntegerField(blank=True, null=True)
    arenalosses2v2 = models.SmallIntegerField(blank=True, null=True)
    streak2v2 = models.SmallIntegerField(blank=True, null=True)
    highestrating2v2 = models.SmallIntegerField(blank=True, null=True)
    valleyKills = models.SmallIntegerField(blank=True, null=True)
    valleyDeaths = models.SmallIntegerField(blank=True, null=True)
    valleyCaps = models.SmallIntegerField(blank=True, null=True)
    valleyWins = models.SmallIntegerField(blank=True, null=True)
    valleyLosses = models.SmallIntegerField(blank=True, null=True)
    deserterTime = models.BigIntegerField(blank=True, null=True)
    title = models.CharField(max_length=20, blank=True, null=True)
    rank = models.CharField(max_length=20)
    avatar = models.ImageField(upload_to='avatars/', blank=True, null=True)
    avatar_sm = models.ImageField(upload_to='avatars/', blank=True, null=True)
    user = models.ForeignKey(User, blank=True, null=True)

    def __unicode__(self):
        return self.name

    #def save(self):
    #    retrieve_avatar.delay(self)
    #    super(Player, self).save()


class Town(models.Model):
    name = models.CharField(max_length=30)
    public = models.BooleanField()
    tag = models.CharField(max_length=10)
    motd = models.CharField(max_length=255)
    owner = models.ForeignKey(Player, blank=True, null=True)
    owner_str = models.CharField(max_length=30)
    members = models.ManyToManyField(Player, related_name="members", blank=True, null=True)
    members_str = models.CharField(max_length=1000, blank=True, null=True)
    subowners = models.ManyToManyField(Player, related_name="subowners", blank=True, null=True)
    subowners_str = models.CharField(max_length=300)

    def __unicode__(self):
        return self.name

    def resolve_players(self):
        print 'Resolving', self.name, "for", self.owner_str
        owner_player = Player.objects.filter(name=self.owner_str)
        if owner_player:
            self.owner = owner_player[0]
        else:
            self.owner = Player.objects.create(name=self.owner_str)
        self.set_many_field(self.members_str, self.members)
        self.set_many_field(self.subowners_str, self.subowners)

        #A terrible hack, but set to none so the view knows when resolve needs calling again.
        self.members_str = None
        self.save()

    def set_many_field(self, source_list, destination_field):
        member_list = [m for m in source_list.split(",") if not m == ""]
        for m in member_list:
            player = Player.objects.filter(name=m)
            if player:
                destination_field.add(player[0])
            else:
                print 'Creating', m
                destination_field.add(Player.objects.create(name=m))
        print '{0} members resolved for {1}'.format(len(member_list), self.name)

    def num_members(self):
        return self.members.count() + self.subowners.count() + 1


class Quote(models.Model):
    text = models.CharField(max_length=300)
    author = models.ForeignKey(Player, blank=True, null=True)
    event = models.CharField(max_length=100)
    event_url = models.URLField(blank=True, null=True)

    def __unicode__(self):
        return self.text


class Thread(models.Model):
    town = models.ForeignKey(Town)
    title = models.CharField(max_length=255)
    author = models.ForeignKey(Player)
    last_updated = models.DateTimeField(auto_now_add=True)
    owner_only = models.BooleanField()

    def num_posts(self):
        return Post.objects.filter(thread=self).count()


class Post(models.Model):
    thread = models.ForeignKey(Thread)
    text = models.TextField()
    author = models.ForeignKey(Player)
    date = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        return self.text

admin.site.register(Quote)
admin.site.register(Post)