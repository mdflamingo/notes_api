from abc import ABC, abstractmethod
from typing import Any

from sqlalchemy import select, update, delete
from sqlalchemy.ext.asyncio import AsyncSession


class AbstractStorage(ABC):
    @abstractmethod
    async def add_one(self, **kwargs):
        raise NotImplementedError

    @abstractmethod
    async def add_many(self, **kwargs):
        raise NotImplementedError

    @abstractmethod
    async def get_one(self, **kwargs):
        raise NotImplementedError

    @abstractmethod
    async def find_all(self, **kwargs):
        raise NotImplementedError

    @abstractmethod
    async def find_many(self, **kwargs):
        raise NotImplementedError

    @abstractmethod
    async def update(self, **kwargs):
        raise NotImplementedError

    @abstractmethod
    async def delete(self, **kwargs):
        raise NotImplementedError


class SQLAlchemyRepository(AbstractStorage):

    model = None
    session: AsyncSession = None

    async def add_one(self, data: dict[Any]) -> model:
        obj = self.model(**data)
        self.session.add(obj)
        await self.session.commit()
        await self.session.refresh(obj)

        return obj

    async def find_all(self) -> list:
        stmt = select(self.model)
        response = await self.session.execute(stmt)
        objects = [obj[0] for obj in response]

        return objects

    async def get_one(self, filter_condition) -> model:
        stmt = select(self.model).filter(filter_condition)
        result = await self.session.execute(stmt)
        obj = result.scalars().first()

        return obj

    async def add_many(self, **kwargs):
        pass

    async def find_many(self, filter_condition):
        stmt = select(self.model).filter(filter_condition)
        response = await self.session.execute(stmt)
        result = [obj[0] for obj in response.all()]

        return result

    async def update(self, filter_condition, values) -> None:
        stmt = (
            update(self.model)
            .where(filter_condition)
            .values(values)
        )
        await self.session.execute(stmt)
        await self.session.commit()

    async def delete(self, filter_condition):
        stmt = delete(self.model).filter(filter_condition)
        await self.session.execute(stmt)
        await self.session.commit()
