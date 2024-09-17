from functools import lru_cache
from uuid import UUID

from fastapi import Depends
from sqlalchemy import update, delete
from sqlalchemy.ext.asyncio import AsyncSession

from db.postgres import get_session
from models.note import Note
from repositiries.base_repository import SQLAlchemyRepository, AbstractStorage


class NoteRepository(SQLAlchemyRepository):
    def __init__(self, session: AsyncSession):
        self.session = session
        self.model = Note

    async def update(self, note_id: UUID, note_fields: dict) -> None:
        stmt = (
            update(self.model)
            .where(self.model.id == note_id)
            .values(**note_fields)
        )
        await self.session.execute(stmt)
        await self.session.commit()

    async def delete(self, obj_id: UUID):
        stmt = delete(self.model).where(self.model.id == obj_id)
        await self.session.execute(stmt)
        await self.session.commit()


@lru_cache()
def get_note_repository(
        session: AsyncSession = Depends(get_session)
) -> AbstractStorage:
    return NoteRepository(session)
