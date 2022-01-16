from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
from .forms import LoginForm
from .models import players, games


def login(request):
    context = {}
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            try:
                room_name = form.cleaned_data['room_name']
                request.session["room_name"] = room_name
            except Exception as e:
                context = {'result': e}
            return redirect("/coup/game")
        else:
            context["errors"] = form.errors
    return render(request, 'coup/coup_login.html', context)


def game(request, game):
    context = {"room_name": request.session["room_name"]}
    return render(request, 'coup/coup_game.html', context)