import datetime
from src import db

class Board(db.Model):
    __tablename__ = "boards"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(255), nullable=False)
    slug = db.Column(db.String(255), unique=True, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    settings = db.Column(db.JSON, nullable=True) # Stores theme, animation_mode, etc.
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.datetime.utcnow)
    
    # Relationships
    user = db.relationship('User', backref=db.backref('boards', lazy=True))

    def __init__(self, title, slug, user_id, settings=None):
        self.title = title
        self.slug = slug
        self.user_id = user_id
        self.settings = settings if settings else {
            'animation_mode': 'masonry',
            'theme_color': 'indigo',
            'scroll_speed': 10
        }
        self.created_at = datetime.datetime.utcnow()

    def to_json(self):
        return {
            'id': self.id,
            'title': self.title,
            'slug': self.slug,
            'user_id': self.user_id,
            'settings': self.settings,
            'created_at': self.created_at.isoformat()
        }
