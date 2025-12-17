from flask import Blueprint, request, jsonify
from src import db
from src.models.board import Board
from src.models.user import User

boards_blueprint = Blueprint('boards', __name__)

def get_user_from_token(request):
    auth_header = request.headers.get('Authorization')
    if auth_header:
        try:
            auth_token = auth_header.split(" ")[1]
        except IndexError:
            return None
    else:
        return None
    
    if auth_token:
        resp = User.decode_auth_token(auth_token)
        if not isinstance(resp, str):
            return resp # Returns user_id
    return None

@boards_blueprint.route('/boards', methods=['POST'])
def add_board():
    user_id = get_user_from_token(request)
    if not user_id:
        return jsonify({'status': 'fail', 'message': 'Invalid token'}), 401

    post_data = request.get_json()
    if not post_data:
        return jsonify({'status': 'fail', 'message': 'Invalid payload'}), 400

    title = post_data.get('title')
    slug = post_data.get('slug')

    try:
        board = Board.query.filter_by(slug=slug).first()
        if not board:
            new_board = Board(
                title=title,
                slug=slug,
                user_id=user_id
            )
            db.session.add(new_board)
            db.session.commit()
            return jsonify({
                'status': 'success',
                'message': 'Board created!',
                'data': new_board.to_json()
            }), 201
        else:
            return jsonify({
                'status': 'fail',
                'message': 'Board slug already exists.'
            }), 400
    except Exception as e:
        print(e)
        return jsonify({'status': 'fail', 'message': 'Error creating board'}), 500

@boards_blueprint.route('/boards', methods=['GET'])
def get_all_boards():
    user_id = get_user_from_token(request)
    if not user_id:
        return jsonify({'status': 'fail', 'message': 'Invalid token'}), 401

    try:
        boards = Board.query.filter_by(user_id=user_id).all()
        return jsonify({
            'status': 'success',
            'data': [board.to_json() for board in boards]
        }), 200
    except Exception as e:
        print(e)
        return jsonify({'status': 'fail', 'message': 'Error fetching boards'}), 500

@boards_blueprint.route('/boards/<int:board_id>', methods=['GET'])
def get_single_board(board_id):
    user_id = get_user_from_token(request)
    if not user_id:
        return jsonify({'status': 'fail', 'message': 'Invalid token'}), 401
    
    try:
        board = Board.query.filter_by(id=board_id, user_id=user_id).first()
        if not board:
             return jsonify({'status': 'fail', 'message': 'Board not found'}), 404
             
        return jsonify({
            'status': 'success',
            'data': board.to_json()
        }), 200
    except Exception as e:
        return jsonify({'status': 'fail', 'message': 'Error fetching board'}), 500

@boards_blueprint.route('/boards/<int:board_id>', methods=['PUT'])
def update_board(board_id):
    user_id = get_user_from_token(request)
    if not user_id:
        return jsonify({'status': 'fail', 'message': 'Invalid token'}), 401
        
    post_data = request.get_json()
    
    try:
        board = Board.query.filter_by(id=board_id, user_id=user_id).first()
        if not board:
             return jsonify({'status': 'fail', 'message': 'Board not found'}), 404
             
        if 'title' in post_data:
            board.title = post_data['title']
        if 'settings' in post_data:
            # Merge existing settings with new ones
            current_settings = board.settings
            current_settings.update(post_data['settings'])
            board.settings = current_settings
            
        db.session.commit()
        
        return jsonify({
            'status': 'success',
            'message': 'Board updated!',
            'data': board.to_json()
        }), 200
    except Exception as e:
        return jsonify({'status': 'fail', 'message': 'Error updating board'}), 500
