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
    room = c.set_player_nick(data["player_id"], data["nick"])
    sio.enter_room(sid, room)
    print("Player {sid} entered room {room}")

@sio.event
def start_game(sid):
    players = c.pick_player()
    sio.emit("start_game", players, room=players[0]["game_id_id"])
    print(f"Game {players[0]['game_id_id']} started by {sio}")


if __name__ == '__main__':
    eventlet.wsgi.server(eventlet.listen(('0.0.0.0', 3000)), app)
