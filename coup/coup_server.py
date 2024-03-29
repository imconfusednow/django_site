#!/usr/bin/env python3
import eventlet
import socketio
import coup_server_functs as c
import random

sio = socketio.Server(cors_allowed_origins='*')
app = socketio.WSGIApp(sio)

actions = {
    "take-1": {"name": "Take 1 Coin", "challenge": False, "block": False, "code": ""},
    "take-3": {"name": "Take 3 Coins (Duke)", "challenge": True, "block": False, "code": "du"},
    "foreign-aid": {"name": "Foreign Aid", "challenge": False, "block": True, "code": "fa"},
    "steal": {"name": "Steal (Captain)", "challenge": True, "block": True, "code": "ca"},
    "assassinate": {"name": "Assassinate", "challenge": True, "block": True, "code": "as"},
    "swap": {"name": "Swap Cards (Ambassador)", "challenge": True, "block": False, "code": "am"},
    "coup": {"name": "Coup!", "challenge": False, "block": False, "code": "cu"},
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
    players, player, room = c.get_players(sid)
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
        next_action(player["player_id"], {
                    "event_type": "", "player": ""}, True)


@sio.event
def rejoin_game(sid, data):
    c.set_player_nick(data["player_id"], sid, data["nick"])
    room = c.sid_to_room(sid)
    players, player, room = c.get_players(sid)
    sio.enter_room(sid, room)
    hands = [h.pop("hand") for h in players]
    no_cards = [len([i for i in h.split(",") if i != ""]) for h in hands]
    data = [players, [hands[0]] + no_cards[1:]]
    send_info(players, sid, data, "rejoin_game")
    print(f"Player {sid} entered room {room}")


@sio.event
def do_action(sid, data):
    next_action(sid, data)


@sio.event
def challenge(sid):
    c.challenge(sid)


@sio.event
def block(sid):
    c.block(sid)


@sio.event
def get_card_swap(sid):
    players, player, room = c.get_players(sid)
    cards = c.get_card_swap(sid, room)
    send_info(players, sid, cards, "get_card_swap")


def next_action(sid, data, computer=False):
    cards = data["cards"] if "cards" in data else []
    event_type = data["event_type"]
    target = data["player"] if "player" in data else ""
    players, player, room = c.get_players(sid)
    if computer:
        event_type = random.choice(list(actions.keys()))
        target = random.choice(players)
        target = target["name"]
        sio.sleep(random.randint(1, 3))
    allow_challenge, allow_block = actions[event_type]["challenge"], actions[event_type]["block"]
    send_action(players, sid, allow_challenge, allow_block, event_type, player)
    has_card = False
    challenged = False
    blocked = False
    if actions[event_type]["challenge"] or actions[event_type]["block"]:
        challenged, blocked, has_card, challenger, blocker, player_num, card_num = c.check_challenged(
            sid, actions[event_type]["code"])
    if challenged:
        send_challenge(players, sid, challenged, has_card,
                       challenger, event_type, player_num, card_num)
    elif blocked:
        send_block(players, sid, challenged, blocker)
        challenged, has_card, challenger, player_num, card_num = c.check_block_challenged(sid, actions[event_type]["code"], blocked)
        if challenged:
            send_challenge(players, sid, challenged, has_card, challenger, event_type, player_num, card_num)

    c.do_action(sid, event_type, bool(
        (challenged and not has_card) or blocked), target, cards, room)
    just_died = c.check_dead(room)
    if just_died:
        sio.emit("lose", [],  just_died)
    next_player = c.next_turn(sid, room)
    players, player, room = c.get_players(sid)
    send_info(players, sid, False, "rejoin_game")
    if next_player["computer"]:
        next_action(next_player["player_id"], {
                    "event_type": "", "player": ""}, True)


def send_info(players, sid, data, method):
    if not data:
        hands = [h.pop("hand") for h in players]
        no_cards = [len([i for i in h.split(",") if i != ""]) for h in hands]
    for i in players:
        if (not data or players[0]["player_id"] == sid) and (not players[0]['computer']):
            if not data:
                sio.emit(method, [players, [hands[0]] +
                                  no_cards[1:]],  to=players[0]["player_id"])

            if data:
                sio.emit(method, data,  to=players[0]["player_id"])
        players.append(players.pop(0))
        if not data:
            hands.append(hands.pop(0))
            no_cards.append(no_cards.pop(0))


def send_action(players, sid, allow_challenge, allow_block, action_type, player):
    for i in players:
        if (not i['computer'] and not i["player_id"] == sid):
            sio.emit("report_action", {"allow_challenge": allow_challenge, "allow_block": allow_block,
                                       "action_type": actions[action_type]["name"], "player": player["name"]},  to=i["player_id"])
        elif i["player_id"] == sid:
            sio.emit("report_action", {
                     "action_type": actions[action_type]["name"], "player": "You"},  to=i["player_id"])
    if allow_challenge or allow_block:
        sio.sleep(8)
    else:
        sio.sleep(2)


def send_challenge(players, sid, player_id, has_card, challenger, action_type, player_num, card_num):
    for i in players:
        player_num_tmp = player_num - i["sequence"] - 1
        if player_num_tmp < 0:
            player_num_tmp += 4
        if (not i['computer'] and i["player_id"] != player_id):
            sio.emit("report_challenge", {"player": challenger, "success": has_card, "action_type": actions[action_type][
                     "code"], "card_num": card_num, "player_num": player_num_tmp, "alive": i["alive"]},  to=i["player_id"])
        elif i["player_id"] == player_id:
            sio.emit("report_challenge", {"player": "You", "success": has_card, "action_type": actions[action_type][
                     "code"], "card_num": card_num, "player_num": player_num_tmp, "alive": i["alive"]},  to=i["player_id"])

    sio.sleep(10)


def send_block(players, sid, player_id, blocker):
    for i in players:
        if (not i['computer'] and not i["player_id"] == sid):
            sio.emit("report_block", {"player": blocker},  to=i["player_id"])
        elif i["player_id"] == sid:
            sio.emit("report_block", {"player": "You"},  to=i["player_id"])
        sio.sleep(8)

if __name__ == '__main__':
    eventlet.wsgi.server(eventlet.listen(('0.0.0.0', 3000)), app)
