import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from flask_bcrypt import Bcrypt
from src.socket import socketio

# Instantiate the extensions
db = SQLAlchemy()
cors = CORS()
bcrypt = Bcrypt()

def create_app(script_info=None):
    # Instantiate the app
    app = Flask(__name__)

    # Set configuration
    app_settings = os.getenv('FLASK_SETTINGS', 'src.config.DevelopmentConfig')
    app.config.from_object(app_settings)

    # Set up extensions
    db.init_app(app)
    cors.init_app(app, resources={r"/*": {"origins": "*"}})
    bcrypt.init_app(app)
    socketio.init_app(app, cors_allowed_origins="*", message_queue=app.config.get('CELERY_BROKER_URL'))

    # Register blueprints (Placeholder for now)
    from src.api.ping import ping_blueprint
    from src.api.auth import auth_blueprint
    from src.api.boards import boards_blueprint
    from src.api.photos import photos_blueprint
    from src.api.static_files import static_blueprint
    from src.api.viewer import viewer_blueprint
    app.register_blueprint(ping_blueprint)
    app.register_blueprint(auth_blueprint)
    app.register_blueprint(boards_blueprint)
    app.register_blueprint(photos_blueprint)
    app.register_blueprint(static_blueprint)
    app.register_blueprint(viewer_blueprint)

    # Shell context for flask cli
    @app.shell_context_processor
    def ctx():
        return {'app': app, 'db': db}

    return app
