import datetime

from django.contrib import admin
from django.contrib.auth.models import User
from django.db import models
from django.db.models import Q
from image_cropping import ImageRatioField, ImageCropField
from tinymce import models as tinymce_models
from unipath import Path

from loka.core.email_messages import issue_comment, issue_status_change


ISSUE_TYPE = (
    ("1", "Bug"),
    ("2", "Feature Request")
)

ISSUE_STATUS = (
    ("1", "New"),
    ("2", "Accepted"),
    ("3", "Rejected"),
    ("4", "Resolved"),
    ("5", "Closed")
)


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
    overloadWins = models.SmallIntegerField(blank=True, null=True)
    overloadLosses = models.SmallIntegerField(blank=True, null=True)
    overloadOverloads = models.SmallIntegerField(blank=True, null=True)
    overloadKills = models.SmallIntegerField(blank=True, null=True)
    overloadDeaths = models.SmallIntegerField(blank=True, null=True)
    overloadScore = models.SmallIntegerField(blank=True, null=True)
    arrowShots = models.SmallIntegerField(blank=True, null=True)
    arrowHits = models.SmallIntegerField(blank=True, null=True)
    title = models.CharField(max_length=20, blank=True, null=True)
    rank = models.CharField(max_length=20, blank=True, null=True)
    avatar = models.ImageField(upload_to='avatars/', blank=True, null=True)
    avatar_sm = models.ImageField(upload_to='avatars/', blank=True, null=True)
    user = models.ForeignKey(User, blank=True, null=True)
    receive_notifications = models.BooleanField(default=False, blank=False)

    def __unicode__(self):
        return self.name

    def check_avatar(self):
        avatar_path = Path("/var/www/loka3/static/media/" + str(self.avatar))
        avatar_sm_path = Path("/var/www/loka3/static/media/" + str(self.avatar_sm))

        print "{} exists: {}".format(avatar_path, avatar_path.exists())

        if not avatar_path.exists() or not avatar_sm_path.exists():
            print "Wiping avatars for", self.name
            self.avatar = None
            self.avatar_sm = None
            self.save()

    def get_1v1_rank(self):
        players = Player.objects.filter(Q(arenawins__gt=0) | Q(arenalosses__gt=0)).order_by("-arenarating")
        return [index for index, player in enumerate(players) if player.name == self.name][0] + 1

    def get_2v2_rank(self):
        players = Player.objects.filter(Q(arenawins2v2__gt=0) | Q(arenalosses2v2__gt=0)).order_by("-arenarating2v2")
        return [index for index, player in enumerate(players) if player.name == self.name][0] + 1

    def get_vota_rank(self):
        players = Player.objects.filter(Q(valleyWins__gt=0) | Q(valleyLosses__gt=0)).order_by("-valleyScore")
        # print 'vota players?', players
        if self in players:
            return [index for index, player in enumerate(players) if player.name == self.name][0] + 1
        else:
            return 0

    def get_overload_rank(self):
        players = Player.objects.filter(Q(overloadWins__gt=0) | Q(overloadLosses__gt=0)).order_by("-overloadScore")
        if self in players:
            return [index for index, player in enumerate(players) if player.name == self.name][0] + 1
        else:
            return 0

    def get_vota_score(self):
        return self.valleyCaps * 3 + self.valleyKills - self.valleyDeaths

    def get_overload_score(self):
        return self.overloadOverloads * 3 + self.overloadKills - self.overloadDeaths

    def get_1v1_color_rank(self):
        return (self.highestrating - 1500) / 50

    def get_2v2_color_rank(self):
        return (self.highestrating2v2 - 1500) / 50

    def has_1v1_history(self):
        return ArenaMatch.objects.filter(Q(winner=self) | Q(loser=self))

    def get_1v1_chart_labels(self):
        matches = ArenaMatch.objects.filter(Q(winner=self) | Q(loser=self)).count()
        labels = ""
        for x in range(matches):
            labels += "'',"
        return labels[:-1]

    def get_1v1_chart_ratings(self):
        matches = ArenaMatch.objects.filter(Q(winner=self) | Q(loser=self))
        print '{} total matches'.format(matches.count())
        labels = ""
        for x in matches:
            print "{}({}) beat {}({}) at {}".format(x.winner.name,
                                                    x.winner_rating,
                                                    x.loser.name,
                                                    x.loser_rating,
                                                    x.date)
            if x.winner.name == self.name:
                # print "{} beat {} while rated {}".format(self.name, x.loser.name, x.winner.arenarating)
                labels += '{0},'.format(x.winner_rating)
            else:
                # print "{} lost to {} while rated {}".format(self.name, x.winner.name, x.loser.arenarating)
                labels += '{0},'.format(x.loser_rating)
        return labels[:-1]


class Achievement(models.Model):
    name = models.CharField(max_length=25)
    category = models.CharField(max_length=30)
    title = models.CharField(max_length=40)
    description = models.CharField(max_length=150)
    type = models.CharField(max_length=15)


class UnlockedAchievement(models.Model):
    player = models.ForeignKey(Player, related_name="unlockedplayerachievement")
    achievement = models.ForeignKey(Achievement)
    date = models.DateTimeField()


class PlayerAchievements(models.Model):
    player = models.ForeignKey(Player, related_name="player")
    achievements = models.ManyToManyField(UnlockedAchievement, related_name="achievements", blank=True, null=True)

    def resolve_achievements(self, achievements_list):
        if achievements_list == "":
            return

        # self.achievements.clear()
        for name, timestamp in achievements_list.iteritems():
            achievement = Achievement.objects.filter(name=name)
            if achievement:
                time = datetime.datetime.fromtimestamp(float(timestamp) / 1000.0)
                unlocked_achievement, created = UnlockedAchievement.objects.get_or_create(player=self.player,
                                                                                          achievement=achievement[0],
                                                                                          date=time)
                # Only add created achievements, otherwise we already have a record of the player having the achievement
                if created:
                    self.achievements.add(unlocked_achievement)
        print 'Achievements resolved for {}'.format(self.player.name)

    def get_total_achievement_percentage(self):
        return int((float(self.achievements.count()) / float(Achievement.objects.count())) * 100.0)

    def get_total_achievement_string(self):
        return "{}/{} {}%".format(self.achievements.count(),
                                  Achievement.objects.count(),
                                  self.get_total_achievement_percentage())


# class Alliance(models.Model):
# name = models.CharField(max_length=40)
# leader = models.ForeignKey(Town)
#     towns = models.ManyToManyField(Town, related_name="alliancetowns")

class Town(models.Model):
    name = models.CharField(max_length=30)
    public = models.BooleanField(default=True)
    description = tinymce_models.HTMLField()
    tag = models.CharField(max_length=10, blank=True, null=True)
    motd = models.CharField(max_length=255, blank=True, null=True)
    owner = models.ForeignKey(Player)
    members = models.ManyToManyField(Player, related_name="members")
    subowners = models.ManyToManyField(Player, related_name="subowners", blank=True, null=True)
    level = models.IntegerField(default=1)
    latitude = models.FloatField()
    longitude = models.FloatField()
    # alliance = models.ForeignKey(Alliance)

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

    def has_territories(self):
        return Territory.objects.filter(town=self).count() > 0


class TownMedia(models.Model):
    town = models.ForeignKey(Town)
    banner = ImageCropField(blank=True, null=True, upload_to='townimages/')
    banner_crop = ImageRatioField('banner', '1250x250', size_warning=True)
    list_banner = ImageCropField(blank=True, null=True, upload_to='townlistimages/')
    list_banner_crop = ImageRatioField('list_banner', '250x150', size_warning=True)


class Territory(models.Model):
    name = models.CharField(max_length=50)
    latitude = models.FloatField()
    longitude = models.FloatField()
    conflicted = models.BooleanField(default=False)
    town = models.ForeignKey(Town)


class Quote(models.Model):
    text = models.CharField(max_length=300)
    author = models.ForeignKey(Player, blank=True, null=True)
    event = models.CharField(max_length=100)
    event_url = models.URLField(blank=True, null=True)

    def __unicode__(self):
        return self.text


class BannerArticle(models.Model):
    title = models.CharField(max_length=50)
    header = models.CharField(max_length=50, blank=True, null=True)
    text = models.CharField(max_length=150)
    url = models.URLField(blank=True, null=True)
    url_text = models.CharField(blank=True, null=True, max_length=30)
    background = models.CharField(max_length=50)

    def __unicode__(self):
        return self.title


class Thread(models.Model):
    town = models.ForeignKey(Town)
    title = models.CharField(max_length=255)
    author = models.ForeignKey(Player)
    last_updated = models.DateTimeField(auto_now_add=True)
    owner_only = models.BooleanField(default=False)

    def num_posts(self):
        return Post.objects.filter(thread=self).count()


class Post(models.Model):
    thread = models.ForeignKey(Thread)
    description = tinymce_models.HTMLField()
    author = models.ForeignKey(Player)
    date = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        return self.text


class Comment(models.Model):
    town = models.ForeignKey(Town)
    text = models.CharField(max_length=400)
    author = models.ForeignKey(Player)
    date = models.DateTimeField(auto_now_add=True)


class ArenaMatch(models.Model):
    date = models.DateTimeField(auto_now_add=True)
    loser = models.ForeignKey(Player, related_name="loser")
    winner = models.ForeignKey(Player, related_name="winner")
    loser_rating = models.IntegerField()
    winner_rating = models.IntegerField()
    rating_change = models.IntegerField()
    loser_damage = models.IntegerField()
    winner_damage = models.IntegerField()
    length = models.IntegerField()


class Issue(models.Model):
    type = models.CharField(max_length=1, choices=ISSUE_TYPE)
    title = models.CharField(max_length=300)
    description = tinymce_models.HTMLField()
    reporter = models.ForeignKey(Player)
    status = models.CharField(max_length=1, choices=ISSUE_STATUS, default=1)
    created = models.DateTimeField(auto_now_add=True)
    resolved = models.DateTimeField(blank=True, null=True)

    def __unicode__(self):
        return self.title

    def send_comment_email(self):
        for commenter in self.get_all_commenters():
            print 'Emailing', commenter.name
            user = User.objects.get(username=commenter.name)
            issue_comment(commenter.name, self.title, self.id,
                          user.email)

    def send_status_change_email(self):
        for commenter in self.get_all_commenters():
            print 'Emailing', commenter.name
            user = User.objects.get(username=commenter.name)
            issue_status_change(commenter.name, self.title, self.id,
                                self.get_status_display(),
                                user.email)

    def get_all_commenters(self):
        comments = IssueComment.objects.filter(issue=self)
        commenters = []
        for comment in comments:
            if not comment.author in commenters:
                commenters.append(comment.author)
        return commenters


class IssueComment(models.Model):
    issue = models.ForeignKey(Issue)
    text = models.CharField(max_length=400)
    author = models.ForeignKey(Player)
    date = models.DateTimeField(auto_now_add=True)


admin.site.register(Quote)
admin.site.register(Issue)
admin.site.register(Player)
admin.site.register(BannerArticle)