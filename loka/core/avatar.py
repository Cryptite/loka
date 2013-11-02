from django.core.files import File
from django.core.files.temp import NamedTemporaryFile
import requests

__author__ = 'tmiller'


def retrieve_avatar(player_model):
    webFile = "https://minotar.net/avatar/%s/%s.png" % (player_model.name, 100)
    print 'Downloading avatar for', player_model.name
    r = requests.get(webFile)

    img_temp = NamedTemporaryFile()
    img_temp.write(r.content)
    img_temp.flush()

    player_model.avatar.save("{0}.png".format(player_model.name), File(img_temp), save=True)
