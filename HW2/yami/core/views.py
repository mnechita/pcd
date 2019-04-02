# Create your views here.
import requests
from django.contrib.auth import login as django_login, authenticate
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.shortcuts import render, redirect
from requests.compat import urljoin

from core.dal import DAL
from core.forms import LoginForm, SignUpForm
from yami.settings import API_ROOT

data_layer = DAL()


def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            # data_layer.create_user(user)
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            django_login(request, user)
            return redirect('home')
    else:
        form = SignUpForm()
    return render(request, 'registration/signup.html', {'form': form})


def login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)

        user = authenticate(username=form.request['username'], password=form.request['password'])

        if user is not None:
            django_login(request, user)
            return redirect('home')
    else:
        form = LoginForm()
    return render(request, 'registration/login.html', {'form': form})


@login_required
def home(request):
    # try:
    #     if request.session['username'] is None:
    #         return redirect('login')
    # except Exception as e:
    #     return redirect('login')
    x = request
    return render(request, 'home.html')


@login_required
def upload(request):
    return render(request, 'upload.html')


@login_required
def view_colection(request):
    page = request.GET.get('page', 1)
    show = request.GET.get('show', 'all')
    sortBy = request.GET.get('sortBy', 'name')
    set = request.GET.get('set', '')
    rarity = request.GET.get('rarity', '')


    if page == 1:
        username = request.user.username
        api_link = 'view-collection'
        resp = requests.get(urljoin(API_ROOT, api_link), params={'username': username})
        cards = resp.json()['body']
        request.session['cards'] = cards
    else:
        cards = request.session['cards']

    if show == 'owned':
        cards = list(filter(lambda x: x['Count'] > 0, cards))
    elif show == 'unowned':
        cards = list(filter(lambda x: x['Count'] == 0, cards))

    if sortBy == 'set':
        cards.sort(key=lambda x: x['Set'])
    if set:
        cards = list(filter(lambda x: x['Set'] == set, cards))
    if rarity:
        cards = list(filter(lambda x: x['Rarity'] == rarity, cards))

    paginator = Paginator(cards, 12)
    try:
        page_cards = paginator.page(page)
    except PageNotAnInteger:
        page_cards = paginator.page(1)
    except EmptyPage:
        page_cards = paginator.page(paginator.num_pages)

    return render(request, 'view-collection.html', context={'cards': page_cards})
