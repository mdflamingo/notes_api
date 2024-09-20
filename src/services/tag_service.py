from functools import lru_cache

from fastapi import Depends

from models.tag import Tag
from repositories.base_repository import AbstractStorage
from repositories.tag_repository import get_tag_repository


class TagService:
    def __init__(self, db: AbstractStorage):
        self.db = db

    async def get_tag(self, tag_name: str):
        filter_stm = (Tag.name == tag_name)
        tag = await self.db.get_one(filter_condition=filter_stm)

        return tag


@lru_cache()
def get_tag_service(
        db: AbstractStorage = Depends(get_tag_repository)
) -> TagService:
    return TagService(db)
