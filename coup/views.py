from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
from .forms import LoginForm
from .models import players, games
import coup.coup_functs as c


def login(request):
    context = {}
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            try:
                room_name = form.cleaned_data['room_name']                
                request.session["room_name"] = room_name
                session_id =  request.session.session_key
                if (form.cleaned_data['submit_type'] == "create"):
                    error = c.add_game(room_name,session_id)
                    if error: raise ValueError(error)
                else:
                    error = c.join_game(room_name,session_id)
                    if error: raise ValueError(error)
            except Exception as e:
                context = {'error': e}
                return render(request, 'coup/coup_login.html', context)
            return redirect("/coup/game")
        else:
            context["errors"] = form.errors
    return render(request, 'coup/coup_login.html', context)


def game(request):
    context = {"room_name": request.session["room_name"], "player_name": ""}
    return render(request, 'coup/coup_game.html', context)