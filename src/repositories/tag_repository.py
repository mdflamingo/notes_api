from functools import lru_cache

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from db.postgres import get_session
from models.tag import Tag
from repositories.base_repository import SQLAlchemyRepository, AbstractStorage


class TagRepository(SQLAlchemyRepository):
    def __init__(self, session: AsyncSession):
        self.session = session
        self.model = Tag


@lru_cache()
def get_tag_repository(
        session: AsyncSession = Depends(get_session)
) -> AbstractStorage:
    return TagRepository(session)
