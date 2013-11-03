from django.core.files import File
from celery.task import task
from loka.core.avatar import download_avatar

__author__ = 'Tom'


@task()
def retrieve_avatar(player_model):
    #Should this get called multiple times perhaps, let's kill it right here.
    if player_model.avatar:
        return

    print 'Downloading avatars for {0}'.format(player_model.name)
    avatar = download_avatar(player_model.name, 100)
    avatar_sm = download_avatar(player_model.name, 30)

    print 'Storing avatars for {0}'.format(player_model.name)
    player_model.avatar.save("{0}.png".format(player_model.name), File(avatar), save=True)
    player_model.avatar_sm.save("{0}_sm.png".format(player_model.name), File(avatar_sm), save=True)