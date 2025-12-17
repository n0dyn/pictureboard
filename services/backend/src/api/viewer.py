from flask import Blueprint, jsonify
from src.models.board import Board
from src.models.photo import Photo
from src.socket import socketio
from flask_socketio import join_room

viewer_blueprint = Blueprint('viewer', __name__)

@viewer_blueprint.route('/view/<slug>', methods=['GET'])
def get_board_data(slug):
    board = Board.query.filter_by(slug=slug).first()
    if not board:
        return jsonify({'status': 'fail', 'message': 'Board not found'}), 404
    
    photos = Photo.query.filter_by(board_id=board.id, status='pending').all() # or 'approved'
    
    return jsonify({
        'status': 'success',
        'data': {
            'board': board.to_json(),
            'photos': [photo.to_json() for photo in photos]
        }
    }), 200

@socketio.on('join')
def on_join(data):
    room = data['room']
    join_room(room)
    print(f'Client joined room: {room}')
