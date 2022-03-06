#!/usr/bin/env python3
import eventlet
import socketio
import coup_server_functs as c
import random

sio = socketio.Server(cors_allowed_origins='*')
app = socketio.WSGIApp(sio)

actions = {
    "take-1": {"name": "Take 1 Coin", "challenge": False, "block": False},
    "take-3": {"name": "Take 3 Coins (Duke)", "challenge": True, "block": False},
    "foreign-aid": {"name": "Foreign Aid", "challenge": False, "block": True},
    "steal": {"name": "Steal (Captain)", "challenge": True, "block": True},
    "assassinate": {"name": "Assassinate", "challenge": True, "block": True},
    "swap": {"name": "Swap Cards (Ambassador)", "challenge": True, "block": False},
}


@sio.event
def connect(sid, environ):
    print('connect ', sid)


@sio.event
def disconnect(sid):
    print('disconnect ', sid)


@sio.event
def join_game(sid, data):
    c.set_player_nick(data["player_id"], sid, data["nick"])
    room = c.sid_to_room(sid)
    players, player = c.get_players(sid)
    sio.enter_room(sid, room)
    send_info(players, sid, False, "join_game")
    print(f"Player {sid} entered room {room}")


@sio.event
def start_game(sid):
    players, player = c.pick_starter(sid)
    c.deal(players)
    send_info(players, sid, False, "start_game")
    print(f"Game {players[0]['game_id_id']} started by {sio}")
    if player["computer"]:
        do_computer_action(player["player_id"])


@sio.event
def rejoin_game(sid, data):
    c.set_player_nick(data["player_id"], sid, data["nick"])
    room = c.sid_to_room(sid)
    players, player = c.get_players(sid)
    sio.enter_room(sid, room)
    send_info(players, sid, True, "rejoin_game")
    print(f"Player {sid} entered room {room}")


@sio.event
def do_action(sid, data):
    players, player = c.get_players(sid)
    allow_challenge, allow_block = actions[data]["challenge"], actions[data]["block"]
    send_action(players, sid, allow_challenge, allow_block, data, player)
    cnb = c.check_action_success(sid)
    next_player = c.do_action(sid, data)
    players, player = c.get_players(sid)
    send_info(players, sid, False, "rejoin_game")
    if next_player["computer"]:
        do_computer_action(next_player["player_id"])

@sio.event
def challenge(sid):
    c.challenge(sid)
    


def do_computer_action(sid):
    data = random.choice(list(actions.keys()))
    sio.sleep(random.randint(1, 3))
    players, player = c.get_players(sid)
    allow_challenge, allow_block = actions[data]["challenge"], actions[data]["block"]
    send_action(players, sid, allow_challenge, allow_block, data, player)
    challenged, blocked, has_card = c.check_challenged(sid)
    if challenged:
        send_challenge(players, sid, challenged, has_card)
    next_player = c.do_action(sid, data)
    players, player = c.get_players(sid)
    send_info(players, sid, False, "rejoin_game")
    if next_player["computer"]:
        do_computer_action(next_player["player_id"])


def send_info(players, sid, only_one, method):
    hands = [h.pop("hand") for h in players]
    no_cards = [len([i for i in h.split(",") if i != ""]) for h in hands]
    for i in players:
        if (not only_one or players[0]["player_id"] == sid) and (not players[0]['computer']):
            sio.emit(method, [players, [hands[0]] +
                              no_cards[1:]],  to=players[0]["player_id"])
            if only_one:
                break
        players.append(players.pop(0))
        hands.append(hands.pop(0))
        no_cards.append(no_cards.pop(0))


def send_action(players, sid, allow_challenge, allow_block, action_type, player):
    for i in players:
        if (not i['computer'] and not i["player_id"] == sid):
            sio.emit("report_action", {"allow_challenge": allow_challenge, "allow_block": allow_block, "action_type": actions[action_type]["name"], "player": player["name"]},  to=i["player_id"])
        elif i["player_id"] == sid:
            sio.emit("report_action", {"action_type": actions[action_type]["name"], "player": "You"},  to=i["player_id"])
    if allow_challenge or allow_block:
        sio.sleep(8)
    else:
        sio.sleep(2)


def send_challenge(players, sid, player, has_card):
    for i in players:
        if (not i['computer'] and not i["player_id"] == sid):
            sio.emit("report_challenge", {"player": player["name"]}, "success": has_card,  to=i["player_id"])
        elif i["player_id"] == sid:
            sio.emit("report_challenge", {"player": "You", "success": has_card},  to=i["player_id"])


if __name__ == '__main__':
    eventlet.wsgi.server(eventlet.listen(('0.0.0.0', 3000)), app)
