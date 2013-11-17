from itertools import chain
import json
from django.contrib import messages, auth
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.core import serializers
from django.core.urlresolvers import reverse
from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.shortcuts import render_to_response, get_object_or_404
from django.template.context import RequestContext
from rest_framework import viewsets
from loka.forms import TownBannerForm

from loka.models import Player, Town, Quote, Post, Thread, Comment, TownMedia
from loka.serializers import TownSerializer
from loka.tasks import retrieve_avatar


class TownViewSet(viewsets.ModelViewSet):
    """
        API endpoint that allows users to be viewed or edited.
        """
    queryset = Town.objects.all()
    serializer_class = TownSerializer


def getavatar(request, player_name):
    player = Player.objects.get(name=player_name)
    retrieve_avatar(player)
    print 'returning', "static/media/{0}".format(player.avatar)
    return HttpResponse(json.dumps({"path": "/static/media/{0}".format(player.avatar)}),
                        mimetype='application/javascript')


def getquote(request):
    quote = Quote.objects.order_by('?')
    print quote
    if quote:
        quote_serialized = serializers.serialize('json', quote)
        quote_serialized += serializers.serialize('json', quote[0].author)
    else:
        quote_serialized = "[]"
    print quote_serialized
    return HttpResponse(quote_serialized,
                        mimetype='application/javascript')


def deleteitem(request, item_id):
    if request.POST['action'] == "post":
        Post.objects.get(id=item_id).delete()
        messages.success(request, 'Post deleted!')
    elif request.POST['action'] == "comment":
        Comment.objects.get(id=item_id).delete()
        messages.success(request, 'Comment deleted!')
    elif request.POST['action'] == "thread":
        thread = Thread.objects.get(id=item_id)
        [post.delete() for post in Post.objects.filter(thread=thread)]
        thread.delete()
        messages.success(request, "Thread deleted!")
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


def pvp(request):
    return render_to_response('pvp.html', RequestContext(request))


def pvp1v1(request):
    players = Player.objects.all().order_by("-arenarating")

    return render_to_response('pvp_1v1.html', RequestContext(request, {
        'players': players,
    }))


def player(request, player_name):
    try:
        player = Player.objects.get(name=player_name)
        return render_to_response('player.html', RequestContext(request, {
            'player': player,
        }))
    except Exception, e:
        raise Http404


def townboard(request, town_name):
    town = Town.objects.get(name=town_name)
    user_in_town = town.members.filter(name=request.user.username)
    print user_in_town
    if not request.user.is_authenticated() and not town.public:
        raise Http404
    elif request.user.is_authenticated() and not town.public and not user_in_town and not request.user.username == "cryptite":
        raise Http404
    threads = Thread.objects.filter(town=town).order_by("-last_updated")

    if request.POST:
        if request.POST['action'] == "public":
            if town.public:
                town.public = False
            else:
                town.public = True
            town.save()
            return HttpResponse({"something": "somethingelse"},
                                mimetype='application/javascript')

        elif request.POST['action'] == "thread":
            author = Player.objects.get(name=request.user.username)
            new_thread = Thread.objects.create(town=town,
                                               title=request.POST['title'],
                                               author=author)
            Post.objects.create(thread=new_thread,
                                text=request.POST['text'],
                                author=author)
    return render_to_response('townboard.html', RequestContext(request, {
        'town': town,
        'threads': threads,
    }))


def townthread(request, town_name, thread_id):
    town = Town.objects.get(name=town_name)
    thread = Thread.objects.get(id=thread_id)
    posts = Post.objects.filter(thread=thread).order_by("-date")

    if request.POST:
        Post.objects.create(thread=thread,
                            text=request.POST['comment'],
                            author=Player.objects.get(name=request.user.username))

    return render_to_response('townthread.html', RequestContext(request, {
        'town': town,
        'thread': thread,
        'posts': posts,
    }))


def townhome(request, town_name):
    town = Town.objects.get(name=town_name)
    image = TownMedia.objects.filter(town=town)
    print image
    if image:
        image = image[0]
    else:
        image = TownMedia.objects.create(town=town)
    print image
    form = TownBannerForm(instance=image)
    user_in_town = town.members.filter(name=request.user.username)
    if not request.user.is_authenticated() and not town.public:
        raise Http404
    elif request.user.is_authenticated() and not town.public and not user_in_town and not request.user.username == "Cryptite":
        raise Http404

    comments = Comment.objects.filter(town=town).order_by("-date")

    if request.POST:
        print request.POST['action']
        if request.POST['action'] == "public":
            if town.public:
                town.public = False
            else:
                town.public = True
            town.save()
            return HttpResponse({town.public: "somethingelse"},
                                mimetype='application/javascript')

        elif request.POST['action'] == "comment":
            author = Player.objects.get(name=request.user.username)
            Comment.objects.create(town=town,
                                   text=request.POST['text'],
                                   author=author)

        elif request.POST['action'] == "banner":
            form = TownBannerForm(request.POST, request.FILES, instance=image)
            if form.is_valid():
                image = form.save()
    return render_to_response('townhome.html', RequestContext(request, {
        'town': town,
        'image': image,
        'form': form,
        'comments': comments,
        'userintown': user_in_town,
    }))


def about(request):
    return render_to_response('about.html', RequestContext(request))


def towns(request):
    return render_to_response('towns.html', RequestContext(request))


def townslist(request):
    #Resolve town members
    [t.resolve_players() for t in Town.objects.all() if t.members_str]

    if request.user.is_authenticated():
        if request.user.username == "Cryptite":
            townlist_query = Town.objects.all()
        else:
            player = Player.objects.filter(name=request.user.username)
            if len(player) == 0:
                player = Player.objects.create(user=request.user, name=request.user.username)
            else:
                player = player[0]
            townlist_query = list(chain(Town.objects.filter(public=1),
                                        Town.objects.filter(public=0, members__in=[player])))
        return render_to_response('townslist.html', RequestContext(request, {
            'towns': townlist_query,
            'player': Player.objects.get(name=request.user.username),
        }))
    else:
        townlist_query = Town.objects.filter(public=1)
        return render_to_response('townslist.html', RequestContext(request, {
            'towns': townlist_query,
        }))


def logout(request):
    auth.logout(request)
    messages.success(request, 'Seeya next time!')
    return render_to_response('index.html', RequestContext(request))


def registration(request, registration_id):
    try:
        user = User.objects.get(password=registration_id)
    except Exception, e:
        messages.warning(request, "You can't do that!")
        return render_to_response("index.html", RequestContext(request))
    print 'Request is for user', user.username
    player = Player.objects.filter(name=user.username)
    if len(player) > 0:
        player = player[0]
        player.user = user
        player.save()
    else:
        player = Player.objects.create(name=user.username, user=user)

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
            #login(request, user)
            return render_to_response('index.html', RequestContext(request, {
                'user': user,
            }))
    return render_to_response('register.html', RequestContext(request, {
        'user': user,
        'player': player,
    }))


def home(request):
    if request.POST:
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, 'Welcome back, {0}!'.format(user.username))
        else:
            messages.warning(request, 'Login information was incorrect. Try again!')
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    elif request.user.is_authenticated():
        return render_to_response('index.html', RequestContext(request, {
            'user': request.user,
        }))
    return render_to_response('index.html', RequestContext(request))