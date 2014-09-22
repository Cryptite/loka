import json

from django.contrib import messages, auth
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.core import serializers
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.db.models import Q
from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.middleware.csrf import get_token
from django.shortcuts import render_to_response, get_object_or_404
from django.template.context import RequestContext
from rest_framework import generics
from rest_framework.status import HTTP_201_CREATED

from loka.core.email_messages import issue_created
from loka.forms import TownBannerForm
from loka.models import Player, Town, Quote, Post, Thread, Comment, TownMedia, ArenaMatch, Issue, BannerArticle, \
    IssueComment, ISSUE_STATUS, Achievement, PlayerAchievements, UnlockedAchievement, Territory, Alliance
from loka.serializers import TownSerializer, UserSerializer, PlayerSerializer, ArenaMatchSerializer, \
    PlayerAchievementsSerializer, AchievementSerializer, resolve_player, TerritorySerializer, AllianceSerializer
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


class AllianceDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Alliance.objects.all()
    serializer_class = AllianceSerializer
    lookup_field = "name"
    towns = ""

    def put(self, request, *args, **kwargs):
        self.towns = request.DATA["towns"]
        return super(AllianceDetail, self).put(request, *args, **kwargs)

    def post_save(self, obj, created=False):
        obj.set_many_field(self.towns, obj.towns)
        super(AllianceDetail, self).post_save(obj, created)


class TerritoryDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Territory.objects.all()
    serializer_class = TerritorySerializer
    lookup_field = "name"


class UserDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    lookup_field = "username"


class PlayerDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Player.objects.all()
    serializer_class = PlayerSerializer
    lookup_field = "name"


class PlayerAchievementsDetail(generics.ListCreateAPIView):
    queryset = PlayerAchievements.objects.all()
    serializer_class = PlayerAchievementsSerializer
    lookup_field = "name"

    def create(self, request, *args, **kwargs):
        data = request.DATA
        player = resolve_player(data["player"])
        player_achievements, created = PlayerAchievements.objects.get_or_create(player=player)
        player_achievements.resolve_achievements(data["achievements"])
        player_achievements.save()

        # This needs to be threaded i think.
        # retrieve_avatar(player)
        return HttpResponse(status=HTTP_201_CREATED)


class ArenaMatchDetail(generics.CreateAPIView):
    queryset = ArenaMatch.objects.all()
    serializer_class = ArenaMatchSerializer


class AchievementDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Achievement.objects.all()
    serializer_class = AchievementSerializer
    lookup_field = "name"


def start(request):
    csrf_token = get_token(request)
    return render_to_response('import.html',
                              {'csrf_token': csrf_token}, context_instance=RequestContext(request))


def get_avatar(request, player_name):
    player = Player.objects.get(name=player_name)
    retrieve_avatar(player)
    return HttpResponse(json.dumps({"path": "/static/media/{0}".format(player.avatar)}),
                        mimetype='application/javascript')


def check_player_avatars(objects):
    for player in objects:
        player.check_avatar()


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
    elif request.POST['action'] == "issuecomment":
        IssueComment.objects.get(id=item_id).delete()
        messages.success(request, 'Comment deleted!')
    elif request.POST['action'] == "thread":
        thread = Thread.objects.get(id=item_id)
        [post.delete() for post in Post.objects.filter(thread=thread)]
        thread.delete()
        messages.success(request, "Thread deleted!")
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


def pvp(request):
    return render_to_response('pvp.html', RequestContext(request))


def map_page(request):
    strength_towns = [town for town in Town.objects.filter(Q(strength__gt=0)).order_by("-strength")]
    return render_to_response('map.html', RequestContext(request, {
        'towns': Town.objects.all(),
        'strength_towns': strength_towns,
        'territories': Territory.objects.all(),
    }))


def pvp1v1(request):
    players = Player.objects.filter(Q(arenawins__gt=0) | Q(arenalosses__gt=0)).order_by("-arenarating")
    check_player_avatars(players)

    paginator = Paginator(players, 25)  # Show 25 contacts per page
    matches = ArenaMatch.objects.order_by("-id")[:5]

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
        'matches': matches
    }))


def pvp2v2(request):
    players = Player.objects.filter(Q(arenawins2v2__gt=0) | Q(arenalosses2v2__gt=0)).order_by("-arenarating2v2")
    check_player_avatars(players)
    return render_to_response('pvp_2v2.html', RequestContext(request, {
        'players': players,
    }))


def pvpvota(request):
    players = Player.objects.filter(Q(valleyWins__gt=0) | Q(valleyLosses__gt=0)).order_by("-valleyScore")
    for p in players:
        p.check_avatar()
        if not p.valleyScore:
            p.valleyScore = p.get_vota_score()
            p.save()

    return render_to_response('pvp_vota.html', RequestContext(request, {
        'players': players,
    }))


def pvpoverload(request):
    players = Player.objects.filter(Q(overloadWins__gt=0) | Q(overloadLosses__gt=0)).order_by("-overloadScore")
    for p in players:
        p.check_avatar()
        if not p.overloadScore:
            p.overloadScore = p.get_overload_score()
            p.save()

    return render_to_response('pvp_overload.html', RequestContext(request, {
        'players': players,
    }))


def player(request, player_name):
    try:
        player = resolve_player(player_name)
        player.check_avatar()
        achievements, created = PlayerAchievements.objects.get_or_create(player=player)
        return render_to_response('player.html', RequestContext(request, {
            'player': player,
            'achievements': achievements
        }))
    except Exception, e:
        print e
        raise Http404


def player_achievements(request, player_name, category):
    try:
        player = Player.objects.get(name=player_name)
        achievements = UnlockedAchievement.objects.filter(player=Player.objects.get(name=player),
                                                          achievement__category=category)

        # Resolve achievements that aren't earned
        achievement_names = [achievement.achievement.name for achievement in achievements]
        locked_achievements = [a for a in Achievement.objects.filter(category=category) if
                               not a.name in achievement_names]

        return render_to_response('player_achievements.html', RequestContext(request, {
            'player': player,
            'category': category,
            'achievements': reversed(achievements),
            'locked_achievements': locked_achievements
        }))
    except Exception, e:
        print e
        raise Http404


def issuelist(request):
    issues = Issue.objects.all().exclude(status="5").order_by("-created")
    closed_issues = Issue.objects.filter(status="5")

    if request.POST:
        if request.POST['action'] == "issue":
            bug_type = 0
            if 'bug' in request.POST:
                bug_type = 1
            elif 'feature' in request.POST:
                bug_type = 2
            author = Player.objects.get(name=request.user.username)
            new_issue = Issue.objects.create(description=request.POST['text'],
                                             title=request.POST['title'],
                                             type=bug_type,
                                             reporter=author)

            issue_created(author.name, new_issue.title, new_issue.id)

            # if town.public:
            # town.public = False
            # else:
            # town.public = True
            # town.save()
            # return HttpResponse({"something": "somethingelse"},
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
        'closed_issues': closed_issues
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

                issue.send_comment_email()

            if request.POST['action'] == "issue":
                if 'bug' in request.POST:
                    issue.type = "1"
                elif 'feature' in request.POST:
                    issue.type = "2"

                for choice_id, choice in ISSUE_STATUS:
                    print choice_id, choice
                    if choice in request.POST:
                        issue.status = choice_id
                        break

                issue.description = request.POST['text']
                issue.title = request.POST['title']
                issue.save()

                issue.send_status_change_email()

        return render_to_response('issue.html', RequestContext(request, {
            'issue': issue,
            'status': issue.get_status_display(),
            'comments': comments,
            'status_choices': ISSUE_STATUS
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


def towngallery(request, town_name):
    town = Town.objects.get(name=town_name)
    user_in_town = town.members.filter(name=request.user.username)
    print user_in_town
    # if not request.user.is_authenticated() and not town.public:
    # raise Http404
    # elif request.user.is_authenticated() and not town.public and not user_in_town and not request.user.username == "cryptite":
    # raise Http404

    return render_to_response('towngallery.html', RequestContext(request, {
        'userintown': user_in_town
    }))


def townthread(request, town_name, thread_id):
    town = Town.objects.get(name=town_name)
    thread = Thread.objects.get(id=thread_id)
    posts = Post.objects.filter(thread=thread).order_by("-date")

    if request.POST:
        Post.objects.create(thread=thread,
                            description=request.POST['comment'],
                            author=Player.objects.get(name=request.user.username))

    return render_to_response('townthread.html', RequestContext(request, {
        'town': town,
        'thread': thread,
        'posts': posts,
    }))


def townhome(request, town_name):
    town = get_object_or_404(Town, name=town_name)
    if town:
        check_player_avatars(town.members.all())

    image = TownMedia.objects.filter(town=town)
    if image:
        image = image[0]
    else:
        image = TownMedia.objects.create(town=town)
    form = TownBannerForm(instance=image)
    user_in_town = town.members.filter(name=request.user.username)
    if request.user.username == "Cryptite" or request.user.username == "Magpieman":
        user_in_town = User.objects.filter(username=request.user.username)
    if not request.user.is_authenticated() and not town.public:
        return render_to_response('townslist.html', RequestContext(request, {
            'towns': Town.objects.filter(public=1),
        }))
    elif request.user.is_authenticated() and not town.public and not user_in_town and not request.user.username == "Cryptite":
        return render_to_response('townslist.html', RequestContext(request, {
            'towns': Town.objects.filter(public=1),
        }))

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

        elif request.POST['action'] == "delete" and request.user.username == "Cryptite":
            print 'Delete', town.name
            town.delete()
            return townslist(request)

    return render_to_response('townhome.html', RequestContext(request, {
        'town': town,
        'image': image,
        'form': form,
        'comments': comments,
        'userintown': user_in_town,
    }))


def about(request):
    return render_to_response('about.html', RequestContext(request))


def guide(request):
    return render_to_response('guide.html', RequestContext(request))


def donate(request):
    return render_to_response('donate.html', RequestContext(request))


def thankyou(request):
    return render_to_response('thankyou.html', RequestContext(request))


def towns(request):
    return render_to_response('towns.html', RequestContext(request))


def townslist(request):
    townlist_query = Town.objects.all().order_by("name")
    alliances = Alliance.objects.all().order_by("name")
    alliance_towns = []
    for alliance in alliances:
        print "Trying", alliance.name
        for town in alliance.towns.all():
            print "Adding", town.name
            alliance_towns.append(town)
    solo_towns = [town for town in townlist_query if not town in alliance_towns]

    # for town in townlist_query:
    # check_player_avatars(town.members.all())

    return render_to_response('townslist.html', RequestContext(request, {
        'alliances': alliances,
        'towns': solo_towns,
        'townmedia': TownMedia.objects.all()
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
            # login(request, user)
            return render_to_response('index.html', RequestContext(request, {
                'user': user,
            }))
    return render_to_response('register.html', RequestContext(request, {
        'user': user,
        'player': player,
    }))


def home(request):
    news = BannerArticle.objects.all()
    print request.POST
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
                           'url': "/player/" + player.name}
            results.append(search_json)
        data = json.dumps(results)
    else:
        data = 'fail'
    mimetype = 'application/json'
    return HttpResponse(data, mimetype)