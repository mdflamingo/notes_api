from functools import lru_cache
from uuid import UUID

from fastapi import Depends
from fastapi.encoders import jsonable_encoder

from models.note import Note
from repositories.base_repository import AbstractStorage
from repositories.note_repository import get_note_repository
from schemas.note_schema import NoteCreate, NoteUpdate


class NoteService:
    def __init__(self, db: AbstractStorage):
        self.db = db

    async def create_note(self, note: NoteCreate):
        note_dict = jsonable_encoder(note)
        note = await self.db.add_one(data=note_dict)

        return note

    async def get_note(self, note_id: UUID):
        filter_stm = (Note.id == note_id)
        note = await self.db.get_one(filter_condition=filter_stm)

        return note

    async def get_notes(self):
        notes = await self.db.find_all()
        test = [note.tags for note in notes]

        return notes, test

    async def update_note(self, note_id: UUID, note_fields: NoteUpdate):
        note_in_db = await self.get_note(note_id=note_id)
        if not note_in_db:
            return None

        note_fields = jsonable_encoder(note_fields)
        await self.db.update(note_id=note_id, note_fields=note_fields)

        return await self.get_note(note_id=note_id)

    async def delete_note(self, note_id: UUID):
        note_in_db = await self.get_note(note_id=note_id)
        if not note_in_db:
            return None

        await self.db.delete(obj_id=note_id)

        return f'Note with id <{note_id}> has been deleted'


@lru_cache()
def get_note_service(
        db: AbstractStorage = Depends(get_note_repository)
) -> NoteService:
    return NoteService(db)
