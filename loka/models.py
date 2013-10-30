from django.contrib import admin
from django.db import models


# Create your models here.
class Player(models.Model):
    name = models.CharField(max_length=30)
    arenarating = models.SmallIntegerField()
    arenawins = models.SmallIntegerField()
    arenalosses = models.SmallIntegerField()
    streak = models.SmallIntegerField()
    highestrating = models.SmallIntegerField()
    arenarating2v2 = models.SmallIntegerField()
    arenawins2v2 = models.SmallIntegerField()
    arenalosses2v2 = models.SmallIntegerField()
    streak2v2 = models.SmallIntegerField()
    highestrating2v2 = models.SmallIntegerField()
    valleyKills = models.SmallIntegerField()
    valleyDeaths = models.SmallIntegerField()
    valleyCaps = models.SmallIntegerField()
    valleyWins = models.SmallIntegerField()
    valleyLosses = models.SmallIntegerField()
    deserterTime = models.BigIntegerField()
    title = models.CharField(max_length=20)
    rank = models.CharField(max_length=20)
    avatar = models.ImageField(upload_to='images/avatars/')

    def __unicode__(self):
        return self.name


class Town(models.Model):
    name = models.CharField(max_length=30)
    public = models.BooleanField()
    tag = models.CharField(max_length=10)
    owner = models.CharField(max_length=30)


class Quote(models.Model):
    text = models.CharField(max_length=300)
    author = models.ForeignKey(Player, blank=True, null=True)
    event = models.CharField(max_length=100)
    event_url = models.URLField(blank=True, null=True)

admin.site.register(Quote)