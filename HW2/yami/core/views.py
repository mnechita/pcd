# Create your views here.

from django.shortcuts import render, redirect

from .forms import *
from .dal import *
import core.models as models

data_layer = DAL()


def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.instance
            data_layer.create_user(user)
            request.session['username'] = user.username

            return redirect('home')
    else:
        form = SignUpForm()
    return render(request, 'registration/signup.html', {'form': form})


def login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)

        user = models.User(form.request['username'], form.request['password'])
        valid = data_layer.check_user(user)

        if valid:
            request.session['username'] = user.username
            return redirect('home')
    else:
        form = LoginForm()
    return render(request, 'registration/login.html', {'form': form})


def home(request):
    # try:
    #     if request.session['username'] is None:
    #         return redirect('login')
    # except Exception as e:
    #     return redirect('login')
    x = request
    return render(request, 'home.html')


def upload(request):
    return render(request, 'upload.html', {'username': request.session['username']})




