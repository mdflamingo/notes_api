from uuid import UUID
from pydantic import BaseModel, Field, ConfigDict


class NoteInDB(BaseModel):
    id: UUID
    title: str
    tags: list

    model_config = ConfigDict(from_attributes=True)


class NoteCreate(BaseModel):
    title: str = Field(min_length=4, max_length=26)
    text: str


class NoteUpdate(BaseModel):
    title: str | None = Field(min_length=4, max_length=26)
    text: str | None
