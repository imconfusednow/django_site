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
                room_name = form.cleaned_data['room_name'].lower()           
                request.session["room_name"] = room_name
                returned = ""              
                if (form.cleaned_data['submit_type'] == "create"):
                    returned = c.add_game(room_name,request.session.get("player_id", None))
                    if "error" in returned: raise ValueError(returned["error"])
                else:
                    returned = c.join_game(room_name,request.session.get("player_id", None))
                    if "error" in returned: raise ValueError(returned["error"])
                request.session["player_id"] = returned["player_id"]
            except Exception as e:
                context = {'error': e}
                return render(request, 'coup/coup_login.html', context)
            return redirect("/coup/game")
        else:
            context["error"] = form.errors[0]
    else:
        name, started = c.get_player(request.session.get("room_name", None), request.session.get("player_id", None))
        if name:
            return redirect("/coup/game")
    return render(request, 'coup/coup_login.html', context)


def game(request):
    context = {"room_name": request.session["room_name"]}
    context["player_name"], context["player_in_started_game"] = c.get_player(request.session.get("room_name", None), request.session.get("player_id", None))
    context["player_id"] = request.session["player_id"]

    return render(request, 'coup/coup_game.html', context)