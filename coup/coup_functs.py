from .models import players, games


def add_game(name, player_id):
    existing = games.objects.filter(name=name)
    if existing.exists():
        return {"error": f"Room already exists, click join to join: {name}"}
    game = games(name=name)
    game.save()
    pk = add_player(game, player_id)
    return {"player_id": pk}


def join_game(name, player_id):
    existing = games.objects.filter(name=name)
    if not existing.exists():
        return {"error": f"Room does not exist, click create to create this room: {name}"}
    existing_players = players.objects.filter(game_id=existing.first())
    if len(existing_players) > 3:
        return {"error": f"Room '{name}' is full"}
    pk = add_player(existing.first(), player_id)
    return {"player_id": pk}


def add_player(room, player_id):
    existing = players.objects.filter(pk=player_id)
    pk = None
    if existing.exists():
        pk = existing[0].pk
    player = players(game_id=room, computer=False, coins=0, pk=player_id)
    if pk:
        player.save(update_fields=["game_id", "computer", "coins"])
    else:
        player.save()
    return player.pk


def get_current_players(room, player_id):
    existing = games.objects.filter(name=room)
    existing_players = players.objects.filter(game_id=existing.first())
    for i in existing_players:
        if existing_players[0].id == player_id: break
        existing_players.append(existing_players.pop(0))
    return existing_players


