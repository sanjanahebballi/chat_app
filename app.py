from flask import Flask, render_template, request, send_from_directory, url_for, jsonify
from flask_socketio import SocketIO, emit, join_room, leave_room
import os
from werkzeug.utils import secure_filename
from datetime import datetime
import base64
import mimetypes
import json

app = Flask(__name__, 
    static_url_path='', 
    static_folder='static',
    template_folder='templates'
)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'secret!')
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'pdf', 'doc', 'docx', 'mp3', 'mp4', 'wav', 'avi'}

# Create uploads directory if it doesn't exist
if not os.path.exists(app.config['UPLOAD_FOLDER']):
    os.makedirs(app.config['UPLOAD_FOLDER'])

socketio = SocketIO(app, cors_allowed_origins="*")
users = {}
rooms = {'general': {'name': 'General Chat', 'messages': []}}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

@socketio.on('connect')
def handle_connect():
    users[request.sid] = {
        'username': f'User_{len(users) + 1}',
        'connected_at': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        'rooms': ['general']
    }
    join_room('general')
    emit('user_list', [{'username': u['username'], 'id': sid} for sid, u in users.items()], broadcast=True)
    emit('room_list', list(rooms.keys()))

@socketio.on('disconnect')
def handle_disconnect():
    if request.sid in users:
        for room in users[request.sid]['rooms']:
            leave_room(room)
        del users[request.sid]
        emit('user_list', [{'username': u['username'], 'id': sid} for sid, u in users.items()], broadcast=True)

@socketio.on('file_upload')
def handle_file_upload(data):
    if request.sid in users:
        username = users[request.sid]['username']
        
        # Handle base64 encoded file data
        if 'file' in data and 'filename' in data:
            try:
                # Get file info
                filename = secure_filename(data['filename'])
                file_data = data['file']
                
                if ';base64,' in file_data:
                    # Split header from base64 data
                    header, encoded = file_data.split(';base64,')
                    file_data = base64.b64decode(encoded)
                
                # Save file
                file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                with open(file_path, 'wb') as f:
                    if isinstance(file_data, str):
                        f.write(file_data.encode())
                    else:
                        f.write(file_data)
                
                # Get file type
                file_type = mimetypes.guess_type(filename)[0] or 'application/octet-stream'
                file_category = file_type.split('/')[0]  # 'image', 'video', 'audio', etc.
                
                # Create message data
                message_data = {
                    'username': username,
                    'message': f'Shared a {file_category}: {filename}',
                    'file': {
                        'name': filename,
                        'url': f'/uploads/{filename}',
                        'type': file_type
                    },
                    'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                    'sender_id': request.sid
                }
                
                # Emit to room or direct message
                room = data.get('room', 'general')
                if room in rooms:
                    rooms[room]['messages'].append(message_data)
                    emit('message', message_data, room=room)
                else:
                    # Direct message to specific user
                    recipient_sid = room
                    if recipient_sid in users:
                        emit('message', message_data, room=recipient_sid)
                        emit('message', message_data, room=request.sid)
                
                return {'status': 'success', 'message': 'File uploaded successfully'}
            
            except Exception as e:
                return {'status': 'error', 'message': str(e)}
    
    return {'status': 'error', 'message': 'Unauthorized'}

@socketio.on('set_username')
def handle_username(username):
    if request.sid in users:
        users[request.sid]['username'] = username
        emit('user_list', [{'username': u['username'], 'id': sid} for sid, u in users.items()], broadcast=True)

@socketio.on('create_room')
def handle_create_room(data):
    room_id = data.get('room_id', f'room_{len(rooms)}')
    room_name = data.get('name', f'Room {len(rooms)}')
    if room_id not in rooms:
        rooms[room_id] = {
            'name': room_name,
            'messages': []
        }
        emit('room_list', list(rooms.keys()), broadcast=True)

@socketio.on('join_room')
def handle_join_room(room_id):
    if room_id in rooms and request.sid in users:
        join_room(room_id)
        users[request.sid]['rooms'].append(room_id)
        emit('room_messages', {'room': room_id, 'messages': rooms[room_id]['messages']})

@socketio.on('leave_room')
def handle_leave_room(room_id):
    if request.sid in users and room_id in users[request.sid]['rooms']:
        leave_room(room_id)
        users[request.sid]['rooms'].remove(room_id)

@socketio.on('message')
def handle_message(data):
    if request.sid in users:
        username = users[request.sid]['username']
        room = data.get('room', 'general')
        message_data = {
            'username': username,
            'message': data['message'],
            'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'sender_id': request.sid
        }
        
        if room in rooms:
            rooms[room]['messages'].append(message_data)
            emit('message', message_data, room=room)
        else:
            recipient_sid = room
            if recipient_sid in users:
                emit('message', message_data, room=recipient_sid)
                emit('message', message_data, room=request.sid)

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    socketio.run(app, host='127.0.0.1', port=port, debug=True, allow_unsafe_werkzeug=True)