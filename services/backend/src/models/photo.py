import datetime
from src import db

class Photo(db.Model):
    __tablename__ = "photos"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    board_id = db.Column(db.Integer, db.ForeignKey('boards.id'), nullable=False)
    filename = db.Column(db.String(255), nullable=False)
    url = db.Column(db.String(500), nullable=False) # S3 or local path
    status = db.Column(db.String(50), default="pending") # pending, approved, rejected
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.datetime.utcnow)

    # Relationships
    board = db.relationship('Board', backref=db.backref('photos', lazy=True))

    def __init__(self, board_id, filename, url, status="pending"):
        self.board_id = board_id
        self.filename = filename
        self.url = url
        self.status = status
        self.created_at = datetime.datetime.utcnow()

    def to_json(self):
        return {
            'id': self.id,
            'board_id': self.board_id,
            'filename': self.filename,
            'url': self.url,
            'status': self.status,
            'created_at': self.created_at.isoformat()
        }
