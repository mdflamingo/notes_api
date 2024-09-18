import os

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


class Settings(BaseSettings):
    postgres_db: str = Field('notes', alias='POSTGRES_DB')
    postgres_port: int = Field(5432, alias='DB_PORT')
    postgres_host: str = Field('postgres', alias='DB_HOST')
    postgres_user: str = Field('postgres', alias='POSTGRES_USER')
    postgres_password: str = Field('123qwe', alias='POSTGRES_PASSWORD')

    redis_host: str = Field('redis', alias='REDIS_HOST')
    redis_port: int = Field(6379, alias='REDIS_PORT')

    authjwt_secret_key: str = Field('secret', alias='AUTH_JWT_SECRET_KEY')

    request_limit_per_minute: int = Field(5, alias='LIMIT')

    logs_dir: str = Field('logs', alias='LOGS_DIR')
    logs_file_name: str = Field('logs/fastapi.json', alias='LOGS_FILE_NAME')
    logs_mode: str = Field('a', alias='LOGS_MODE')
    logs_max_bytes: int = Field(15000000, alias='LOGS_MAX_BYTES')
    logs_backup_count: int = Field(5, alias='BACKUP_COUNT')

    model_config = SettingsConfigDict(
        env_file=os.path.join(os.path.dirname(__file__), '.env'),
        env_file_encoding='utf-8')


settings = Settings()
