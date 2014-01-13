from django.contrib import admin
from django.contrib.auth.models import User
from django.db import models
from django.db.models import Q
from image_cropping import ImageRatioField, ImageCropField


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
    valleyScore = models.SmallIntegerField(blank=True, null=True)
    title = models.CharField(max_length=20, blank=True, null=True)
    rank = models.CharField(max_length=20, blank=True, null=True)
    avatar = models.ImageField(upload_to='avatars/', blank=True, null=True)
    avatar_sm = models.ImageField(upload_to='avatars/', blank=True, null=True)
    user = models.ForeignKey(User, blank=True, null=True)
    receive_notifications = models.BooleanField(default=False, blank=False)

    def __unicode__(self):
        return self.name

    def get_1v1_rank(self):
        players = Player.objects.filter(Q(arenawins__gt=1) | Q(arenalosses__gt=1)).order_by("-arenarating")
        return [index for index, player in enumerate(players) if player.name == self.name][0] + 1

    def get_2v2_rank(self):
        players = Player.objects.filter(Q(arenawins2v2__gt=1) | Q(arenalosses2v2__gt=1)).order_by("-arenarating2v2")
        return [index for index, player in enumerate(players) if player.name == self.name][0] + 1

    def get_vota_rank(self):
        players = Player.objects.filter(Q(valleyWins__gt=1) | Q(valleyLosses__gt=1)).order_by("-valleyKills")
        return [index for index, player in enumerate(players) if player.name == self.name][0] + 1

    def get_1v1_color_rank(self):
        return (self.highestrating - 1500) / 50

    def get_2v2_color_rank(self):
        return (self.highestrating2v2 - 1500) / 50


class Town(models.Model):
    name = models.CharField(max_length=30)
    public = models.BooleanField(default=False)
    tag = models.CharField(max_length=10, blank=True, null=True)
    motd = models.CharField(max_length=255, blank=True, null=True)
    owner = models.ForeignKey(Player)
    members = models.ManyToManyField(Player, related_name="members")
    subowners = models.ManyToManyField(Player, related_name="subowners", blank=True, null=True)

    def __unicode__(self):
        return self.name

    def set_many_field(self, source_list, destination_field):
        if source_list == "":
            return

        member_list = [m for m in source_list.split(",") if not m == ""]
        destination_field.clear()
        for m in member_list:
            player = Player.objects.filter(name=m)
            if player:
                destination_field.add(player[0])
            else:
                print 'Creating', m
                destination_field.add(Player.objects.create(name=m))
        print '{0} members resolved for {1}'.format(len(member_list), self.name)

    def num_members(self):
        return self.members.count()

    def num_threads(self):
        return len(Thread.objects.filter(town=self))

    def num_comments(self):
        return len(Comment.objects.filter(town=self))


class TownMedia(models.Model):
    town = models.ForeignKey(Town)
    banner = ImageCropField(blank=True, null=True, upload_to='townimages/')
    banner_crop = ImageRatioField('banner', '1250x250', size_warning=True)
    list_banner = ImageCropField(blank=True, null=True, upload_to='townlistimages/')
    list_banner_crop = ImageRatioField('list_banner', '250x150', size_warning=True)


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


class Comment(models.Model):
    town = models.ForeignKey(Town)
    text = models.CharField(max_length=400)
    author = models.ForeignKey(Player)
    date = models.DateTimeField(auto_now_add=True)


admin.site.register(Quote)