from django.contrib import messages, auth
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.shortcuts import render_to_response
from django.template.context import RequestContext

from bootstrap_toolkit.widgets import BootstrapUneditableInput

from loka.models import Player, Town


def towns(request):
    return render_to_response('towns.html', RequestContext(request))


def townslist(request):
    towns = Town.objects.filter(public=1)
    return render_to_response('townslist.html', RequestContext(request, {
        'towns': towns,
    }))

def pvp(request):
    return render_to_response('pvp.html', RequestContext(request))


def pvp1v1(request):
    players = Player.objects.all().order_by("-arenarating")
    return render_to_response('pvp_1v1.html', RequestContext(request, {
        'players': players,
    }))


def player(request, player_name):
    player = Player.objects.get(name=player_name)
    return render_to_response('player.html', RequestContext(request, {
        'player': player,
    }))

def town(request, town_name):
    town = Town.objects.get(name=town_name)
    return render_to_response('town.html', RequestContext(request, {
        'town': town,
    }))

def dashboard(request, player_name):
    player = Player.objects.get(name=player_name)
    return render_to_response('player.html', RequestContext(request, {
        'player': player,
    }))


def registration(request, registration_id):
    user = User.objects.get(password=registration_id)
    if request.POST:
        pass1 = request.POST['password']
        pass2 = request.POST['password2']
        if pass1 != pass2:
            messages.warning(request, 'Passwords do not match!')
        else:
            user.set_password(pass1)
            messages.success(request, 'Welcome to Loka!')
            user.save()
            user = authenticate(username=user.username, password=user.password)
            return render_to_response('index.html', RequestContext(request, {
                'player': user,
            }))
    return render_to_response('register.html', RequestContext(request, {
        'player': user,
    }))


def logout(request):
    auth.logout(request)
    messages.success(request, 'Seeya next time!')
    return render_to_response('index.html', RequestContext(request))


def home(request):
    if request.POST:
        username = request.POST['username']
        password = request.POST['password']
        print username, password
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            print 'success'
            # Redirect to a success page.
        else:
            print 'invalid'
            pass
            # Return an 'invalid login' error message.
    elif request.user.is_authenticated():
        return render_to_response('index.html', RequestContext(request, {
            'user': request.user,
        }))
    return render_to_response('index.html', RequestContext(request))