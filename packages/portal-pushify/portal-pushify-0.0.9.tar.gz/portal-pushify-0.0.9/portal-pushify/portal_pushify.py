####### Credits Bojan Radojevic #########
############## techstreets ##############

import os
import sys
import json
import logging
from flask import Flask, request, jsonify, render_template
from flask_socketio import SocketIO, join_room
from gevent import monkey
monkey.patch_all()

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
logger.addHandler(logging.StreamHandler())

NAMESPACE = os.getenv('SOCKET_NAMESPACE', '/wsock')

app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('FLASK_SECRET_KEY', 'secret!')
socketio = SocketIO(app)
socketio.async_mode('gevent')

sessions = {}

@app.route('/')
def app_index():
    return render_template('index.html')

@app.route('/push/<room>', methods=['POST'])
def app_push(room=None):
  is_json = request.is_json
  data = request.get_json() if is_json else request.data
  # print("%s %s" % (is_json, json.loads(data.decode('utf8'))))
  content = data
  if is_json and content and 'message' in content:
    msg = {
      'message': content['message'],
      'room': room
    }
    
    logger.info('Push content to %s: %r', room, content)
    socketio.emit('output', msg, room=room, namespace=NAMESPACE)

    return jsonify({'status': 'OK'}), 200
  else: 
    print('Must push json formated data and message!', file=sys.stderr)
    return jsonify({
      'error': 'Must push json formated data and message!'
    }), 400


@app.route('/<plugin>/push/<room>', methods=['POST'])
def portal_push(plugin=None, room=None):
  is_json = request.is_json
  data = request.get_json() if is_json else request.data

  content = data
  if is_json and content and 'message' in content:
    msg = content['message']

    full_msg = {
      'room': room,
      'message': msg
    }

    logger.info('Push content to %s: %r', room, content)
    socketio.emit('output', full_msg, room=plugin+room, namespace=NAMESPACE)

    return jsonify({'status': 'OK'}), 200
  else:
    return jsonify({
        'error': 'Must push json formated data and message!'
    }), 400


@socketio.on('join', namespace=NAMESPACE)
def subscribe(payload):
  room = payload['room']
  join_room(room)
  

@socketio.on('leave', namespace=NAMESPACE)
def unsubscribe(payload):
  room = payload['room']
  socketio.leave_room(room)


@socketio.on('push', namespace=NAMESPACE)
def push(payload):
  logger.info('Message from client %s', payload)
  print(payload, file=sys.stderr)
  room = payload['room']
  msg = { 'message': payload['message'], 'room': room}
  socketio.emit('output', payload, room=room, namespace=NAMESPACE)
  
  
if __name__ == '__main__':
    socketio.run(app)
