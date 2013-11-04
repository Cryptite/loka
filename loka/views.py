from itertools import chain
from django.contrib import messages, auth
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.db.models import Q
from django.http import HttpResponse, Http404
from django.shortcuts import render_to_response
from django.template.context import RequestContext
from rest_framework import viewsets
import simplejson

from loka.models import Player, Town, Quote, Discussion
from loka.tasks import retrieve_avatar
from serializers import TownSerializer


class TownViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = Town.objects.all()
    serializer_class = TownSerializer


def pvp(request):
    return render_to_response('pvp.html', RequestContext(request))


def pvp1v1(request):
    players = Player.objects.all().order_by("-arenarating")

    #Retrieve avatars for players without them.
    [retrieve_avatar.delay(p) for p in players if not p.avatar]

    return render_to_response('pvp_1v1.html', RequestContext(request, {
        'players': players,
        "quote": Quote.objects.order_by('?')[0],
    }))


def player(request, player_name):
    player = Player.objects.get(name=player_name)
    return render_to_response('player.html', RequestContext(request, {
        'player': player,
    }))


def town(request, town_name):
    town = Town.objects.get(name=town_name)
    user_in_town = town.members.filter(name=request.user.username)
    print user_in_town
    if not request.user.is_authenticated() and not town.public:
        raise Http404
    elif request.user.is_authenticated() and not town.public and not user_in_town and not request.user.username == "cryptite":
        raise Http404
    comments = Discussion.objects.filter(town=town).order_by("-date")

    #Retrieve avatars for players without them.
    [retrieve_avatar.delay(p) for p in town.members.all() if not p.avatar]
    [retrieve_avatar.delay(p) for p in town.subowners.all() if not p.avatar]

    if request.POST:
        if request.POST['action'] == "public":
            if town.public:
                town.public = False
            else:
                town.public = True
            town.save()
            return HttpResponse(simplejson.dumps({"something": "somethingelse"}),
                                mimetype='application/javascript')
        elif request.POST['action'] == "Post comment":
            Discussion.objects.create(town=town,
                                      text=request.POST['comment'],
                                      author=Player.objects.get(name=request.user.username))
    return render_to_response('town.html', RequestContext(request, {
        'town': town,
        'comments': comments,
    }))


def towns(request):
    return render_to_response('towns.html', RequestContext(request))


def townslist(request):
    if request.user.is_authenticated():
        if request.user.username == "cryptite":
            townlist_query = Town.objects.all()
        else:
            player = Player.objects.get(name=request.user.username)
            townlist_query = list(chain(Town.objects.filter(public=1),
                                        Town.objects.filter(public=0, members__in=[player])))
    else:
        townlist_query = Town.objects.filter(public=1)

    #Resolve town members
    [t.resolve_players() for t in townlist_query if t.members_str]

    #Retrieve avatars for players without them.
    [retrieve_avatar.delay(p.owner) for p in townlist_query if not p.owner.avatar]

    return render_to_response('townslist.html', RequestContext(request, {
        'towns': townlist_query,
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
    return render_to_response('index.html', RequestContext(request))
    #quote = Quote.objects.order_by('?')[0]
    #if quote.author and not quote.author.avatar:
    #    retrieve_avatar.delay(quote.author)
    #
    #if request.POST:
    #    username = request.POST['username']
    #    password = request.POST['password']
    #    print username, password
    #    user = authenticate(username=username, password=password)
    #    if user is not None:
    #        login(request, user)
    #        print 'success'
    #        # Redirect to a success page.
    #    else:
    #        print 'invalid'
    #        pass
    #        # Return an 'invalid login' error message.
    #elif request.user.is_authenticated():
    #    return render_to_response('index.html', RequestContext(request, {
    #        'user': request.user,
    #        "quote": Quote.objects.order_by('?')[0],
    #    }))
    #return render_to_response('index.html', RequestContext(request, {
    #    "quote": Quote.objects.order_by('?')[0],
    #}))