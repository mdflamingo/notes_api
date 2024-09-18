from functools import lru_cache

from fastapi import Depends

from db.postgres import get_session
from sqlalchemy.ext.asyncio import AsyncSession

from models.user import User
from repositories.base_repository import SQLAlchemyRepository, AbstractStorage


class UserRepository(SQLAlchemyRepository):
    def __init__(self, session: AsyncSession):
        self.session = session
        self.model = User


@lru_cache()
def get_user_repository(
        session: AsyncSession = Depends(get_session),
) -> AbstractStorage:
    return UserRepository(session)
