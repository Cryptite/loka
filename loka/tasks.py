from django.core.files import File
from celery.task import task
from unipath import Path

from loka.core.avatar import download_avatar
from loka.models import Player
import settings


__author__ = 'Tom'


def delete_avatar(player_model):
    avatar = Path(settings.MEDIA_ROOT, str(player_model.avatar))
    avatar_sm = Path(settings.MEDIA_ROOT, str(player_model.avatar_sm))
    avatar.remove()
    avatar_sm.remove()


@task()
def retrieve_avatar(player_model):
    # Should this get called multiple times perhaps, let's kill it right here.
    if player_model.avatar:
        delete_avatar(player_model)

    print 'Downloading avatars for {0}'.format(player_model.name)
    avatar = download_avatar(player_model.name, 100)
    avatar_sm = download_avatar(player_model.name, 30)

    print 'Storing avatars for {0}'.format(player_model.name)
    player_model.avatar.save("{0}.png".format(player_model.name), File(avatar), save=True)
    player_model.avatar_sm.save("{0}_sm.png".format(player_model.name), File(avatar_sm), save=True)


@task()
def cleanup_avatars():
    for player in Player.objects.all():
        if player.avatar:
            delete_avatar(player)

        player.avatar = None
        player.avatar_sm = None
        player.save()
    print "wiped {} player avatars".format(Player.objects.all().count())