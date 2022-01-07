#!/usr/bin/env python3
import eventlet
import socketio

sio = socketio.Server(cors_allowed_origins='*')
app = socketio.WSGIApp(sio)

@sio.event
def connect(sid, environ):
    print('connect ', sid)


@sio.event
def disconnect(sid):
    print('disconnect ', sid)


@sio.event
def send_message(sid, data):
    msg = data['msg']
    sio.emit('send_result', {'result': msg})


if __name__ == '__main__':
    eventlet.wsgi.server(eventlet.listen(('0.0.0.0', 3000)), app)
