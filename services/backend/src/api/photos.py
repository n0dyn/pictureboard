from flask import Blueprint, request, jsonify, current_app
from werkzeug.utils import secure_filename
import os
from src import db
from src.models.board import Board
from src.models.photo import Photo
from src.socket import socketio
# from src.tasks import process_image # Will implement later

photos_blueprint = Blueprint('photos', __name__)

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@photos_blueprint.route('/upload/<slug>', methods=['POST'])
def upload_file(slug):
    # 1. Check if board exists
    board = Board.query.filter_by(slug=slug).first()
    if not board:
        return jsonify({'status': 'fail', 'message': 'Board not found.'}), 404

    # 2. Check if file is present
    if 'file' not in request.files:
        return jsonify({'status': 'fail', 'message': 'No file part.'}), 400
    
    file = request.files['file']
    if file.filename == '':
        return jsonify({'status': 'fail', 'message': 'No selected file.'}), 400
    
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        
        # Ensure upload dir exists
        if not os.path.exists(current_app.config['UPLOAD_FOLDER']):
             os.makedirs(current_app.config['UPLOAD_FOLDER'])

        save_path = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)
        file.save(save_path)
        
        # Save to DB
        # For now, serving local static files is tricky without Nginx setup properly or using Flask send_from_directory.
        # We will store a relative URL.
        # Ensure backend serves this static folder or nginx does. 
        # For dev simplicity: http://localhost:5001/static/uploads/filename
        
        relative_url = f'http://localhost:5001/static/uploads/{filename}' 
        
        new_photo = Photo(
            board_id=board.id,
            filename=filename,
            url=relative_url,
            status='pending' # or 'approved' if not moderated
        )
        db.session.add(new_photo)
        db.session.commit()
        
        # Emit event to room (room name = board slug)
        socketio.emit('new_photo', new_photo.to_json(), room=slug)
        
        return jsonify({
            'status': 'success',
            'message': 'File uploaded successfully',
            'data': new_photo.to_json()
        }), 201

    return jsonify({'status': 'fail', 'message': 'Invalid file type.'}), 400
