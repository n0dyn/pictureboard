from flask import Blueprint, send_from_directory, current_app
import os

static_blueprint = Blueprint('static_files', __name__)

@static_blueprint.route('/static/uploads/<path:filename>')
def serve_uploads(filename):
    return send_from_directory(current_app.config['UPLOAD_FOLDER'], filename)
