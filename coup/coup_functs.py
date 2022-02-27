from .models import players, games, decks
import random


def add_game(name, player_id):
    log(f"Adding game {name}", True)
    existing = games.objects.filter(name=name)
    if existing.exists():
        return {"error": f"Room already exists, click join to join: {name}"}
    game = games(name=name)
    game.save()
    pk = add_player(game, player_id)
    add_deck(game)
    return {"player_id": pk}


def join_game(name, player_id):
    existing = games.objects.filter(name=name)
    if not existing.exists():
        return {"error": f"Room does not exist, click create to create this room: {name}"}
    if existing.first().started:
        return {"error": f"Game has already started for this room: {name}"}
    existing_players = players.objects.filter(game_id=existing.first())
    if len(existing_players) > 3:
        return {"error": f"Room '{name}' is full"}
    pk = add_player(existing.first(), player_id)
    return {"player_id": pk}


def add_player(room, player_id):
    existing = players.objects.filter(pk=player_id)
    pk = None
    if player_id and existing.exists():
        pk = existing[0].pk
    player = players(game_id=room, computer=False, coins=0, pk=player_id)
    if pk:
        player.save(update_fields=["game_id", "computer", "coins"])
    else:
        player.save()
    return player.pk


def get_player(room, player_id):
    if not (room and player_id):
        return ["", False]
    existing = games.objects.filter(name=room)
    if not (existing.exists()):
        return ["", False]
    existing = existing.first()
    player = players.objects.filter(game_id=existing, pk=player_id)
    if not player.exists():
        return ["", False]
    player = player.first()
    name = player.name
    in_game = True if name and existing.started else False
    return [name, in_game]


def add_deck(game):
    cards = ["co"] * 3 + ["du"] * 3 + ["ca"] * 3 + ["as"] * 3 + ["am"] * 3
    random.shuffle(cards)
    decks.objects.filter(game_id=game).delete()
    for c in cards:
        deck = decks(game_id=game, card_type=c)
        deck.save()


def log(msg, wipe=False):
    write_type = "w" if wipe else "a"
    file = open("/home/imconfusednow/log.log", write_type)
    time = str(datetime.datetime.now())
    file.write(f"[{time}] - {msg} \n")
    file.close()