import uuid
from datetime import datetime

from sqlalchemy import UUID, Column, String, Text, DateTime, ForeignKey
from sqlalchemy.orm import relationship

from db.postgres import Base


class Note(Base):
    __tablename__ = 'notes'
    __table_args = {'extend_existing': True}

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, unique=True, nullable=False)
    user_id = Column(UUID, ForeignKey('users.id', ondelete='CASCADE'), index=True)
    user = relationship('User', backref='user_notes')
    title = Column(String(255), nullable=False)
    text = Column(Text, nullable=True)
    created_date = Column(DateTime, default=datetime.utcnow)
    updated_date = Column(DateTime, default=datetime.utcnow)
    tags = relationship('Tag', secondary='note_tags',
                        back_populates='notes', lazy='selectin', cascade='all, delete')

    def __int__(self, title: str):
        self.title = title

    def __repr__(self) -> str:
        return f'Note {self.title}'


class NoteTag(Base):
    __tablename__ = 'note_tags'
    __table_args = {'extend_existing': True}

    note_id = Column('note_id', ForeignKey('notes.id', ondelete='CASCADE'), primary_key=True)
    tag_id = Column('tag_id', ForeignKey('tags.id', ondelete='CASCADE'), primary_key=True)
