from itertools import chain
import json

from django.contrib import messages, auth
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.core import serializers
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.db.models import Q
from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.middleware.csrf import get_token
from django.shortcuts import render_to_response
from django.template.context import RequestContext
from rest_framework import generics

from loka.forms import TownBannerForm
from loka.models import Player, Town, Quote, Post, Thread, Comment, TownMedia, ArenaMatch, Issue, BannerArticle, \
    IssueComment
from loka.serializers import TownSerializer, UserSerializer, PlayerSerializer, ArenaMatchSerializer
from loka.tasks import retrieve_avatar


class TownDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Town.objects.all()
    serializer_class = TownSerializer
    lookup_field = "name"
    members = ""
    subowners = ""

    def put(self, request, *args, **kwargs):
        self.members = request.DATA["members"]
        self.subowners = request.DATA["subowners"]
        return super(TownDetail, self).put(request, *args, **kwargs)

    def post_save(self, obj, created=False):
        obj.set_many_field(self.members, obj.members)
        obj.set_many_field(self.subowners, obj.subowners)
        super(TownDetail, self).post_save(obj, created)


class UserDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    lookup_field = "username"


class PlayerDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Player.objects.all()
    serializer_class = PlayerSerializer
    lookup_field = "name"


class ArenaMatchDetail(generics.CreateAPIView):
    queryset = ArenaMatch.objects.all()
    serializer_class = ArenaMatchSerializer


def start(request):
    csrf_token = get_token(request)
    return render_to_response('import.html',
                              {'csrf_token': csrf_token}, context_instance=RequestContext(request))


def get_avatar(request, player_name):
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
    players = Player.objects.filter(Q(arenawins__gt=1) | Q(arenalosses__gt=1)).order_by("-arenarating")
    paginator = Paginator(players, 25)  # Show 25 contacts per page

    page = request.GET.get('page')
    try:
        players = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        players = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        players = paginator.page(paginator.num_pages)

    return render_to_response('pvp_1v1.html', RequestContext(request, {
        'players': players,
    }))


def pvp2v2(request):
    players = Player.objects.filter(Q(arenawins2v2__gt=1) | Q(arenalosses2v2__gt=1)).order_by("-arenarating2v2")

    return render_to_response('pvp_2v2.html', RequestContext(request, {
        'players': players,
    }))


def pvpvota(request):
    players = Player.objects.filter(Q(valleyWins__gt=1) | Q(valleyLosses__gt=1)).order_by("-valleyScore")
    for p in players:
        if not p.valleyScore:
            p.valleyScore = p.get_vota_score()
            p.save()

    return render_to_response('pvp_vota.html', RequestContext(request, {
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


def issuelist(request):
    issues = Issue.objects.all().order_by("-created")

    if request.POST:
        if request.POST['action'] == "issue":
            type = 0
            if 'bug' in request.POST:
                type = 1
            elif 'feature' in request.POST:
                type = 2
            author = Player.objects.get(name=request.user.username)
            Issue.objects.create(description=request.POST['text'],
                                 title=request.POST['title'],
                                 type=type,
                                 reporter=author)

            #     if town.public:
            #         town.public = False
            #     else:
            #         town.public = True
            #     town.save()
            #     return HttpResponse({"something": "somethingelse"},
            #                         mimetype='application/javascript')
            #
            # elif request.POST['action'] == "thread":
            #     author = Player.objects.get(name=request.user.username)
            #     new_thread = Thread.objects.create(town=town,
            #                                        title=request.POST['title'],
            #                                        author=author)
            #     Post.objects.create(thread=new_thread,
            #                         text=request.POST['text'],
            #                         author=author)
    return render_to_response('issues.html', RequestContext(request, {
        'issues': issues,
    }))


def issue(request, issue_id):
    try:
        issue = Issue.objects.get(id=issue_id)
        comments = IssueComment.objects.filter(issue=issue)

        if request.POST:
            if request.POST['action'] == "comment":
                author = Player.objects.get(name=request.user.username)
                IssueComment.objects.create(issue=issue,
                                            text=request.POST['text'],
                                            author=author)

                # send_mail('Subject here', 'Here is the message.', 'from@example.com',
                #           [User.objects.get(username=issue.reporter.name).email], fail_silently=False)

            if request.POST['action'] == "issue":
                type = 0
                if 'bug' in request.POST:
                    type = 1
                elif 'feature' in request.POST:
                    type = 2

                issue.description = request.POST['text']
                issue.title = request.POST['title']
                issue.type = type
                issue.save()

            if request.POST['action'] == "close":
                issue.status = 5
                issue.save()

        return render_to_response('issue.html', RequestContext(request, {
            'issue': issue,
            'status': issue.get_status_display(),
            'comments': comments
        }))
    except Exception, e:
        print e
        raise Http404


def townforum(request, town_name):
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
                                description=request.POST['text'],
                                author=author)
    return render_to_response('townforum.html', RequestContext(request, {
        'town': town,
        'threads': threads,
        'userintown': user_in_town
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
    if image:
        image = image[0]
    else:
        image = TownMedia.objects.create(town=town)
    form = TownBannerForm(instance=image)
    user_in_town = town.members.filter(name=request.user.username)
    if request.user.username == "Cryptite":
        user_in_town = User.objects.filter(username="Cryptite")
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

        elif request.POST['action'] == "description":
            town.description = request.POST['description']
            town.save()

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
    if request.user.is_authenticated():
        if request.user.username == "Cryptite":
            townlist_query = Town.objects.all().order_by("name")
        else:
            player = Player.objects.filter(name=request.user.username)
            if len(player) == 0:
                player = Player.objects.create(user=request.user, name=request.user.username)
            else:
                player = player[0]
            townlist_query = list(chain(Town.objects.filter(public=1),
                                        Town.objects.filter(public=0, members__in=[player]).order_by("name")))
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
    news = BannerArticle.objects.all()
    print news
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
        check_player_exists(request.user.username)
        return render_to_response('index.html', RequestContext(request, {
            'user': request.user,
            'news': news,
        }))
    return render_to_response('index.html', RequestContext(request, {
        "news": news,
    }))


def check_player_exists(name):
    player_obj, created = Player.objects.get_or_create(name=name)
    if created:
        print 'Created: ', player_obj, created
        retrieve_avatar(player_obj)


def search(request):
    if request.is_ajax():
        q = request.GET.get('term', '')
        players = Player.objects.filter(name__icontains=q)[:20]
        results = []
        for player in players:
            search_json = {'id': player.id,
                           'label': player.name,
                           'value': player.name,
                           'url': "player/" + player.name}
            results.append(search_json)
        data = json.dumps(results)
    else:
        data = 'fail'
    mimetype = 'application/json'
    return HttpResponse(data, mimetype)