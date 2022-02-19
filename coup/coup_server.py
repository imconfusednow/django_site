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
    c.send_info(players, sid, False, "join_game")   
    print(f"Player {sid} entered room {room}")


@sio.event
def start_game(sid):
    players = c.get_players(True, sid)
    c.deal(players)    
    c.send_info(players, sid, False, "start_game")
    print(f"Game {players[0]['game_id_id']} started by {sio}")


@sio.event
def rejoin_game(sid, data):
    c.set_player_nick(data["player_id"], sid, data["nick"])
    room = c.sid_to_room(sid)
    players = c.get_players(False, sid)
    sio.enter_room(sid, room)    
    c.send_info(players, sid, True, "rejoin_game")   
    print(f"Player {sid} entered room {room}")





if __name__ == '__main__':
    eventlet.wsgi.server(eventlet.listen(('0.0.0.0', 3000)), app)
