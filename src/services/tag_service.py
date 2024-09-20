from functools import lru_cache

from fastapi import Depends

from repositories.base_repository import AbstractStorage
from repositories.tag_repository import get_tag_repository


class TagService:
    def __init__(self, db: AbstractStorage):
        self.db = db


@lru_cache()
def get_tag_service(
        db: AbstractStorage = Depends(get_tag_repository)
) -> TagService:
    return TagService(db)
