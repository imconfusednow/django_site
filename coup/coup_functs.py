from .models import players, games

def add_game(name):
    existing = games.objects.filter(name=name)
    if existing.exists():
        return f"Room already exists, click join to join this room: {name}"
    game = games(name=name)
    game.save()
    return ""