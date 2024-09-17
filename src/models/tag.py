import uuid

from sqlalchemy import UUID, Column, String
from sqlalchemy.orm import relationship

from db.postgres import Base


class Permission:
    pass


class Tag(Base):
    __tablename__ = 'tags'
    __table_args = {'extend_existing': True}

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, unique=True, nullable=False)
    name = Column(String(255), unique=True, nullable=False)

    def __int__(self, name: str, description: str):
        self.name = name

    def __repr__(self) -> str:
        return f'Tag {self.name}'
