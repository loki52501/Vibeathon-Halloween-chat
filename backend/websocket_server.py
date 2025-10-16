import socketio
import asyncio
from typing import Dict, Set
import json
from datetime import datetime

# Create SocketIO server
sio = socketio.AsyncServer(
    cors_allowed_origins=["http://localhost:3000"],
    logger=True,
    engineio_logger=True
)

# Store active connections
active_connections: Dict[str, Set[str]] = {}  # username -> set of room_ids
user_rooms: Dict[str, str] = {}  # username -> current_room

@sio.event
async def connect(sid, environ):
    print(f"Client {sid} connected")

@sio.event
async def disconnect(sid):
    print(f"Client {sid} disconnected")
    # Clean up user connections
    for username, rooms in active_connections.items():
        if sid in rooms:
            rooms.remove(sid)
            if not rooms:
                del active_connections[username]
            break

@sio.event
async def join_chat(sid, data):
    """Handle user joining a chat room"""
    username = data.get('username')
    target_username = data.get('targetUsername')
    
    if not username or not target_username:
        return
    
    # Create room ID for the chat
    room_id = f"chat_{min(username, target_username)}_{max(username, target_username)}"
    
    # Join the room
    await sio.enter_room(sid, room_id)
    
    # Store connection info
    if username not in active_connections:
        active_connections[username] = set()
    active_connections[username].add(sid)
    user_rooms[username] = room_id
    
    # Notify others in the room
    await sio.emit('user_joined', {
        'username': username,
        'timestamp': datetime.now().isoformat()
    }, room=room_id, skip_sid=sid)

@sio.event
async def message(sid, data):
    """Handle incoming messages"""
    username = data.get('sender')
    target_username = data.get('targetUsername')
    message_text = data.get('text')
    
    if not username or not target_username or not message_text:
        return
    
    # Create room ID
    room_id = f"chat_{min(username, target_username)}_{max(username, target_username)}"
    
    # Prepare message data
    message_data = {
        'id': data.get('id'),
        'text': message_text,
        'sender': username,
        'timestamp': data.get('timestamp'),
        'room_id': room_id
    }
    
    # Send message to all users in the room
    await sio.emit('message', message_data, room=room_id)

@sio.event
async def leave_chat(sid, data):
    """Handle user leaving a chat room"""
    username = data.get('username')
    
    if username in user_rooms:
        room_id = user_rooms[username]
        
        # Leave the room
        await sio.leave_room(sid, room_id)
        
        # Notify others in the room
        await sio.emit('user_left', {
            'username': username,
            'timestamp': datetime.now().isoformat()
        }, room=room_id, skip_sid=sid)
        
        # Clean up
        if username in active_connections:
            active_connections[username].discard(sid)
            if not active_connections[username]:
                del active_connections[username]
        
        if username in user_rooms:
            del user_rooms[username]

# Create the SocketIO app
socket_app = socketio.ASGIApp(sio)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(socket_app, host="0.0.0.0", port=8001)
