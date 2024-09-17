import uuid
from datetime import datetime

from sqlalchemy import UUID, Column, String, Text, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from werkzeug.security import check_password_hash, generate_password_hash

from db.postgres import Base


class User(Base):
    __tablename__ = 'users'
    __table_args__ = {'extend_existing': True}

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, unique=True, nullable=False)
    login = Column(String(255), unique=True, nullable=False)
    password = Column(String(255), nullable=False)
    first_name = Column(String(50))
    last_name = Column(String(50))
    created_at = Column(DateTime, default=datetime.utcnow)
    roles = relationship('Role', secondary='user_roles', back_populates='users', lazy='selectin')

    def __init__(self, login: str, password: str, first_name: str, last_name: str) -> None:
        self.login = login
        self.password = generate_password_hash(password)
        self.first_name = first_name
        self.last_name = last_name

    def check_password(self, password: str) -> bool:
        return check_password_hash(self.password, password)

    def __repr__(self) -> str:
        return f'<User {self.login}>'
