import logging
from functools import lru_cache
from http import HTTPStatus
from uuid import UUID

from fastapi import Depends, HTTPException
from fastapi.encoders import jsonable_encoder

from models.note import Note
from models.tag import Tag
from models.user import User
from repositories.base_repository import AbstractStorage
from repositories.note_repository import get_note_repository
from schemas.note_schema import NoteCreate, NoteUpdate
from services.tag_service import TagService, get_tag_service
from services.user_service import UserService, get_user_service


class NoteService:
    def __init__(self, db: AbstractStorage,
                 tag_service: TagService,
                 user_service: UserService):
        self.db = db
        self.tag_service = tag_service
        self.user_service = user_service

    async def create_note(self, note: NoteCreate, user_id: str):
        if not await self.user_service.db.get_one(filter_condition=User.id == user_id):
            raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail='User not found')

        tags = []
        for tag in note.tags:
            tag_db = await self.tag_service.get_tag(tag_name=tag.name)
            if tag_db:
                tags.append(tag_db)
            else:
                tags.append(Tag(name=tag.name))

        note_dict = {
            'user_id': user_id,
            'title': note.title,
            'text': note.text,
            'tags': tags
        }
        note = await self.db.add_one(data=note_dict)

        return note

    async def get_note(self, note_id: UUID, user_id: str):
        filter_stm = (Note.id == note_id) & (Note.user_id == user_id)
        note = await self.db.get_one(filter_condition=filter_stm)

        return note

    async def get_notes(self, user_id: str):
        notes = await self.db.find_all(filter_condition=Note.user_id == user_id)
        return notes

    async def update_note(self, note_id: UUID, note_fields: NoteUpdate, user_id: str):
        note_in_db = await self.get_note(note_id=note_id, user_id=user_id)
        if not note_in_db:
            return None

        note_fields = jsonable_encoder(note_fields)
        await self.db.update(note_id=note_id, note_fields=note_fields)

        return await self.get_note(note_id=note_id, user_id=user_id)

    async def delete_note(self, note_id: UUID, user_id: str):
        note_in_db = await self.get_note(note_id=note_id, user_id=user_id)
        if not note_in_db:
            return None

        await self.db.delete(obj_id=note_id)

        return f'Note with id <{note_id}> has been deleted'


@lru_cache()
def get_note_service(
        db: AbstractStorage = Depends(get_note_repository),
        tag_service: TagService = Depends(get_tag_service),
        user_service: UserService = Depends(get_user_service)
) -> NoteService:
    return NoteService(db, tag_service, user_service)
