from flask import Flask, render_template
from flask_socketio import SocketIO, join_room, leave_room, emit
import logging

app = Flask(__name__)
socketio = SocketIO(app)

# Set up logging
logging.basicConfig(level=logging.INFO)

@app.route('/')
def index():
    return render_template('index.html')  # Ensure this points to your updated HTML file

# Handle joining a room
@socketio.on('join')
def handle_join(data):
    """
    Handles when a user joins a room.
    Expected payload: {'room': <room_name>, 'username': <username>}
    """
    room = data.get('room')
    username = data.get('username')
    if room and username:
        join_room(room)
        logging.info(f'{username} has joined the room {room}')
        emit('user_joined', {'username': username, 'msg': f'{username} has joined the room'}, room=room)
    else:
        logging.warning('Join event received with missing data.')

# Handle leaving a room
@socketio.on('leave')
def handle_leave(data):
    """
    Handles when a user leaves a room.
    Expected payload: {'room': <room_name>, 'username': <username>}
    """
    room = data.get('room')
    username = data.get('username')
    if room and username:
        leave_room(room)
        logging.info(f'{username} left the room {room}')
        emit('user_left', {'username': username, 'msg': f'{username} has left the room'}, room=room)
    else:
        logging.warning('Leave event received with missing data.')

# Handle WebRTC offer from the client
@socketio.on('offer')
def handle_offer(data):
    """
    Handles WebRTC offers.
    Expected payload: {'room': <room_name>, 'offer': <offer_data>}
    """
    try:
        room = data.get('room')
        offer = data.get('offer')
        if room and offer:
            emit('offer', data, room=room)
            logging.info(f'Offer sent to room {room}')
        else:
            logging.warning('Offer event received with missing data.')
    except Exception as e:
        logging.error(f'Error handling offer: {e}')

# Handle WebRTC answer from the client
@socketio.on('answer')
def handle_answer(data):
    """
    Handles WebRTC answers.
    Expected payload: {'room': <room_name>, 'answer': <answer_data>}
    """
    try:
        room = data.get('room')
        answer = data.get('answer')
        if room and answer:
            emit('answer', data, room=room)
            logging.info(f'Answer sent to room {room}')
        else:
            logging.warning('Answer event received with missing data.')
    except Exception as e:
        logging.error(f'Error handling answer: {e}')

# Handle ICE candidate from the client
@socketio.on('ice-candidate')
def handle_ice_candidate(data):
    """
    Handles ICE candidate events.
    Expected payload: {'room': <room_name>, 'candidate': <candidate_data>}
    """
    try:
        room = data.get('room')
        candidate = data.get('candidate')
        if room and candidate:
            emit('ice-candidate', data, room=room)
            logging.info(f'ICE candidate sent to room {room}')
        else:
            logging.warning('ICE candidate event received with missing data.')
    except Exception as e:
        logging.error(f'Error handling ICE candidate: {e}')

# Handle chat messages
@socketio.on('chat-message')
def handle_chat_message(data):
    """
    Handles chat messages.
    Expected payload: {'room': <room_name>, 'username': <username>, 'message': <message>}
    """
    room = data.get('room')
    username = data.get('username')
    message = data.get('message')
    if room and username and message:
        emit('chat-message', {'username': username, 'message': message}, room=room)
        logging.info(f'{username} sent a message to room {room}')
    else:
        logging.warning('Chat message event received with missing data.')

if __name__ == '__main__':
    socketio.run(app, debug=True)
