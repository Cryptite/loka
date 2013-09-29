from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.forms.formsets import formset_factory
from django.shortcuts import render_to_response
from django.template.context import RequestContext
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage

from bootstrap_toolkit.widgets import BootstrapUneditableInput

from .forms import TestForm, TestModelForm, TestInlineForm, WidgetsForm, FormSetInlineForm
from loka.models import Player


def towns(request):
    layout = request.GET.get('layout')
    if not layout:
        layout = 'vertical'
    if request.method == 'POST':
        form = TestForm(request.POST)
        form.is_valid()
    else:
        form = TestForm()
    form.fields['title'].widget = BootstrapUneditableInput()
    return render_to_response('towns.html', RequestContext(request, {
        'form': form,
        'layout': layout,
    }))


def pvp(request):
    layout = request.GET.get('layout')
    if not layout:
        layout = 'vertical'
    if request.method == 'POST':
        form = TestForm(request.POST)
        form.is_valid()
    else:
        form = TestForm()
    form.fields['title'].widget = BootstrapUneditableInput()
    return render_to_response('pvp.html', RequestContext(request, {
        'form': form,
        'layout': layout,
    }))


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
    return render_to_response('index.html', RequestContext(request))