from uuid import UUID

from pydantic import BaseModel, Field, ConfigDict


class UserCreate(BaseModel):
    login: str = Field(min_length=3)
    password: str = Field(min_length=5, max_length=24)
    first_name: str
    last_name: str


class UserInDB(BaseModel):
    id: UUID
    first_name: str
    last_name: str

    model_config = ConfigDict(from_attributes=True)


class UserLogin(BaseModel):
    login: str = Field(min_length=3)
    password: str = Field(min_length=5, max_length=24)
