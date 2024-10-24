from app import db

class Conversation(db.Model):
    __tablename__ = 'conversations'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    session_id = db.Column(db.String(120), unique=True, nullable=False)
    created_at = db.Column(db.TIMESTAMP, server_default=db.func.now())  # Timestamp when the conversation was created
    updated_at = db.Column(db.TIMESTAMP, server_default=db.func.now(), onupdate=db.func.now())  # Timestamp when the conversation was last updated

    # Add relationship to messages with cascade delete
    messages = db.relationship('Message', cascade='all, delete-orphan', backref='conversation', lazy=True)


class Message(db.Model):
    __tablename__ = 'messages'

    id = db.Column(db.Integer, primary_key=True)
    conversation_id = db.Column(db.Integer, db.ForeignKey('conversations.id', ondelete='CASCADE'), nullable=False)  # Foreign key to conversation, with cascade on delete
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)  # User for querying purposes
    messages = db.Column(db.JSON, nullable=False)  # Store message batch as JSON
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp(), nullable=False)
