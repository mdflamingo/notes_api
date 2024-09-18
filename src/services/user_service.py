import logging
import re
from functools import lru_cache
from http import HTTPStatus
from uuid import UUID

from fastapi import Depends, HTTPException, Request
from fastapi.encoders import jsonable_encoder

from db.base_cache import AsyncCache
from db.cache import get_async_cache
from models.user import User
from repositories.base_repository import AbstractStorage
from repositories.user_repository import get_user_repository
from schemas.user_schema import UserCreate, UserLogin


class UserService:
    def __init__(self, db: AbstractStorage,
                 cache: AsyncCache,):
        self.db = db
        self.cache = cache

    async def create_user(self, user_create: UserCreate) -> User:

        user_dict = jsonable_encoder(user_create)
        user = await self.db.add_one(data=user_dict)

        return user

    async def login_user(self, current_user: UserLogin, request):
        user_login = current_user.login
        user = await self.db.get_one(filter_condition=User.login == user_login)
        if user and user.check_password(current_user.password):
            return str(user.id)

        return None

    async def logout_user(self, access_token: dict, current_user) -> str | None:

        user_db = await self.db.get_one(filter_condition=User.id == current_user)
        if user_db:
            await self.db.update(filter_condition=User.id == user_db.id, values={'refresh_token': None})

        ttl = access_token['exp'] - access_token['iat']
        key = access_token.get('jti')

        await self.cache.put(key=key, ttl=ttl, value=True)

        return 'The exit was completed successfully!'


@lru_cache()
def get_user_service(
        db: AbstractStorage = Depends(get_user_repository),
        cache: AsyncCache = Depends(get_async_cache)
) -> UserService:
    return UserService(db, cache)


