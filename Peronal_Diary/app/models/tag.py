"""
Tag — normalized tag for notes.
Many-to-Many with Notes via NoteTag junction table.
"""
from app.extensions import db


class Tag(db.Model):
    __tablename__ = 'tag'

    tag_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(50), nullable=False, unique=True)

    def __repr__(self):
        return f'<Tag {self.tag_id}: {self.name}>'
