from django.shortcuts import render
from django.http import HttpResponseRedirect
from .forms import LoginForm



def login(request):
    context = {}
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            context = {}
            try:
                game_id = form.cleaned_data['game_id']
                
                context = {'game_id': game_id}
            except Exception as e:
                context = {'result': e}
            return HttpResponseRedirect("/coup/game")
    else:
        return render(request, 'coup/coup_login.html', context)


def game(request):
    context = {}
    return render(request, 'coup/coup_game.html', context)