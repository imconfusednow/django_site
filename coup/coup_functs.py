from .models import players, games

def add_game(name,player_id):
    existing = games.objects.filter(name=name)
    if existing.exists():
        return {"error":"Room does not exist, click create to create this room: {name}"}
    game = games(name=name)
    game.save()
    pk = add_player(game, player_id)
    return {"pk":pk}

def join_game(name, player_id):
    existing = games.objects.filter(name=name)
    if not existing.exists():
        return {"error":"Room does not exist, click create to create this room: {name}"}
    pk = add_player(existing.first(), player_id)
    return {"pk":pk}

def add_player(room, player_id):
    existing = players.objects.filter(pk=player_id)
    pk = None
    if existing.exists():
        pk = existing[0].pk
    player = players(game_id=room, session_id=session_id, computer=False, coins=0, pk=pk)
    player.save()
    return player.pk