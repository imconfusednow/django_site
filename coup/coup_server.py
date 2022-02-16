#!/usr/bin/env python3
import eventlet
import socketio
import coup_server_functs as c

sio = socketio.Server(cors_allowed_origins='*')
app = socketio.WSGIApp(sio)

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
    players = c.get_players(False, sid)
    sio.enter_room(sid, room)
    for i in players:
        sio.emit("join_game", players, to=players[0]["player_id"])
        players.append(players.pop(0))        
    print(f"Player {sid} entered room {room}")


@sio.event
def start_game(sid):
    players = c.get_players(True, sid)
    c.deal(players)
    for i in players:
        sio.emit("start_game", players, to=players[0]["player_id"])
        players.append(players.pop(0))        
    print(f"Game {players[0]['game_id_id']} started by {sio}")


@sio.event
def rejoin_game(sid, data):
    c.set_player_nick(data["player_id"], sid, data["nick"])
    room = c.sid_to_room(sid)
    players = c.get_players(False, sid)
    sio.enter_room(sid, room)
    for i in players:
        players.append(players.pop(0))
        if players[0]["player_id"] == sid:
            sio.emit("rejoin_game", players, to=players[0]["player_id"])
    print(f"Player {sid} entered room {room}")

if __name__ == '__main__':
    eventlet.wsgi.server(eventlet.listen(('0.0.0.0', 3000)), app)
