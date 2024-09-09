from app import db

class Entry(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text, nullable=False)
    upvotes = db.Column(db.Integer, default=0)
    downvotes = db.Column(db.Integer, default=0)
    
    # ... existing code ...
    
    def to_dict(self):
        return {
            'id': self.id,
            'content': self.content,
            'upvotes': self.upvotes,
            'downvotes': self.downvotes
        }