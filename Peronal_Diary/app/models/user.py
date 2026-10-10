"""
User model — central entity.
All user-owned data cascades from this table.
"""
from app.extensions import db
from datetime import datetime


class User(db.Model):
    __tablename__ = 'user'

    user_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(150), nullable=False, unique=True)
    password_hash = db.Column(db.LargeBinary(256), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, nullable=True, onupdate=datetime.utcnow)
    last_login = db.Column(db.DateTime, nullable=True)
    is_active = db.Column(db.Boolean, default=True)
    language = db.Column(db.String(10), default='en')
    timezone = db.Column(db.String(50), default='Asia/Karachi')
    profile_notes = db.Column(db.String(500), nullable=True)

    # ── One-to-Many Relationships ──────────────────────────────
    persons = db.relationship('Person', backref='user', lazy='dynamic',
                              cascade='all, delete-orphan')
    locations = db.relationship('Location', backref='user', lazy='dynamic',
                                cascade='all, delete-orphan')
    notes = db.relationship('Notes', backref='user', lazy='dynamic',
                            cascade='all, delete-orphan')
    events = db.relationship('Event', backref='user', lazy='dynamic',
                             cascade='all, delete-orphan')
    reminders = db.relationship('Reminder', backref='user', lazy='dynamic',
                                cascade='all, delete-orphan')
    attachments = db.relationship('Attachment', backref='user', lazy='dynamic',
                                  cascade='all, delete-orphan')
    items = db.relationship('Item', backref='user', lazy='dynamic',
                            cascade='all, delete-orphan')
    documents = db.relationship('Document', backref='user', lazy='dynamic',
                                cascade='all, delete-orphan')
    raw_text_logs = db.relationship('RawTextLog', backref='user', lazy='dynamic',
                                    cascade='all, delete-orphan')
    voice_entries = db.relationship('VoiceEntry', backref='user', lazy='dynamic',
                                    cascade='all, delete-orphan')
    transactions = db.relationship('TransactionLog', backref='user', lazy='dynamic',
                                   cascade='all, delete-orphan')
    assets = db.relationship('Asset', backref='user', lazy='dynamic',
                             cascade='all, delete-orphan')
    file_uploads = db.relationship('FileUpload', backref='user', lazy='dynamic',
                                   cascade='all, delete-orphan')
    knowledge_triples = db.relationship('KnowledgeTriple', backref='user', lazy='dynamic',
                                        cascade='all, delete-orphan')
    quran_listens = db.relationship('UserQuranListen', backref='user', lazy='dynamic',
                                    cascade='all, delete-orphan')

    def __repr__(self):
        return f'<User {self.user_id}: {self.email}>'
