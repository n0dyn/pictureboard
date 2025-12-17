from flask.cli import FlaskGroup
from src import create_app, db
from src.models.user import User
from src.models.board import Board
from src.models.photo import Photo
from src.socket import socketio

app = create_app()
cli = FlaskGroup(create_app=create_app)

@cli.command('recreate_db')
def recreate_db():
    db.drop_all()
    db.create_all()
    db.session.commit()

@cli.command('run_socketio')
def run_socketio():
    socketio.run(app, host='0.0.0.0', port=5000, allow_unsafe_werkzeug=True)

if __name__ == '__main__':
    cli()
