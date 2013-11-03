from django.core.files.temp import NamedTemporaryFile
import requests

__author__ = 'tmiller'


def download_avatar(name, size):
    url = "https://minotar.net/avatar/%s/%s.png" % (name, size)
    r = requests.get(url)

    img_temp = NamedTemporaryFile()
    img_temp.write(r.content)
    img_temp.flush()
    return img_temp
