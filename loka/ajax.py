from dajax.core import Dajax
from dajaxice.decorators import dajaxice_register
import simplejson

__author__ = 'Tom'

@dajaxice_register
def multiply(request, a, b):
    dajax = Dajax()
    result = int(a) * int(b)
    dajax.assign('#result','value',str(result))
    return dajax.json()

@dajaxice_register
def lol(request):
    return simplejson.dumps({'message': 'lol'})