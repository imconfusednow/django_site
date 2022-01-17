from .models import players, games

def add_game(name):
    existing = games.objects.filter(name=name)
    if existing.exists():
        return f"Room already exists, click join to join this room: {name}"
    game = games(name=name)
    game.save()
    add_player(game, session_id)
    return ""

def join_game(name, session_id):
    existing = games.objects.filter(name=name)
    if not existing.exists():
        return f"Room does not exist, click create to create this room: {name}"
    add_player(existing, session_id)

def add_player(room, session_id):
    existing = players.objects.get(session_id=session_id)
    pk = None
    if existing.exists():
        pk = existing[0].pk
    player = players(game_id=room, session_id=session_id, computer=False, coins=0, pk=pk)
    player.save()