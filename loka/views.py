from itertools import chain
import json
from django.contrib import messages, auth
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.core import serializers
from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template.context import RequestContext

from loka.models import Player, Town, Quote, Post, Thread, Comment
from loka.tasks import retrieve_avatar


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


def townthread(request, town_name, thread_id):
    print town_name, thread_id
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


def townhome(request, town_name):
    town = Town.objects.get(name=town_name)
    user_in_town = town.members.filter(name=request.user.username)
    if not request.user.is_authenticated() and not town.public:
        raise Http404
    elif request.user.is_authenticated() and not town.public and not user_in_town and not request.user.username == "cryptite":
        raise Http404

    comments = Comment.objects.filter(town=town)

    if request.POST:
        if request.POST['action'] == "public":
            if town.public:
                town.public = False
            else:
                town.public = True
            town.save()
            return HttpResponse({"something": "somethingelse"},
                                mimetype='application/javascript')

        elif request.POST['action'] == "comment":
            author = Player.objects.get(name=request.user.username)
            Comment.objects.create(town=town,
                                   text=request.POST['text'],
                                   author=author)
    return render_to_response('townhome.html', RequestContext(request, {
        'town': town,
        'comments': comments,
    }))


def towns(request):
    return render_to_response('towns.html', RequestContext(request))


def townslist(request):
    if request.user.is_authenticated():
        if request.user.username == "Cryptite":
            townlist_query = Town.objects.all()
        else:
            player = Player.objects.filter(user=request.user)
            if len(player) == 0:
                player = Player.objects.create(user=request.user, name=request.user.username)
            else:
                player = player[0]
            townlist_query = list(chain(Town.objects.filter(public=1),
                                        Town.objects.filter(public=0, members__in=[player])))
    else:
        townlist_query = Town.objects.filter(public=1)

    #Resolve town members
    [t.resolve_players() for t in Town.objects.all() if t.members_str]

    print townlist_query

    return render_to_response('townslist.html', RequestContext(request, {
        'towns': townlist_query,
    }))


def getavatar(request, player_name):
    player = Player.objects.get(name=player_name)
    retrieve_avatar(player)
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


def registration(request, registration_id):
    try:
        user = User.objects.get(password=registration_id)
    except Exception, e:
        messages.warning(request, "No such player can be registered that way.")
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
            return render_to_response('index.html', RequestContext(request, {
                'user': user,
                'player': player,
            }))
    return render_to_response('register.html', RequestContext(request, {
        'user': user,
        'player': player,
    }))


def logout(request):
    auth.logout(request)
    messages.success(request, 'Seeya next time!')
    return render_to_response('index.html', RequestContext(request))


def getavatar(request, player_name):
    player = Player.objects.get(name=player_name)
    retrieve_avatar(player)
    print 'returning', "static/media/{0}".format(player.avatar)
    return HttpResponse(json.dumps({"path": "/static/media/{0}".format(player.avatar)}),
                        mimetype='application/javascript')


def home(request):
    return render_to_response('index_live.html', RequestContext(request))
    if request.POST:
        username = request.POST['username']
        password = request.POST['password']
        print username, password
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