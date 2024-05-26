import secrets
import string
from functools import lru_cache

from dotenv import load_dotenv
from pydantic import Field, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict

load_dotenv()
env_file = "../.env"
encoding = "utf-8"


def generate_secret(byte=512):
    return secrets.token_urlsafe(byte)


def generate_aes_key(length=32):
    alphabet = string.ascii_letters + string.digits
    return "".join(secrets.choice(alphabet) for i in range(length))


SECRET_KEY_32 = f"{generate_secret(32)}"
SECRET_KEY_64 = f"{generate_secret(64)}"
SECRET_KEY_32_AES = f"{generate_aes_key(32)}"


class DbSettings(BaseSettings):
    model_config = SettingsConfigDict(
        title="DB Settings",
        env_file=env_file,
        env_file_encoding=encoding,
    )
    POSTGRES_DSN: str = Field(alias="DATABASE_URL")


class ApiSettings(BaseSettings):
    model_config = SettingsConfigDict(
        title="API Settings",
        env_file=env_file,
        env_file_encoding=encoding,
    )
    API_V1_PREFIX: str = "/api/v1"
    API_KEY: str = Field(default=f"{SECRET_KEY_32}")
    API_SECRET: str = Field(default=f"{SECRET_KEY_32}")


class Settings(BaseSettings):
    DATABASE: DbSettings = DbSettings()
    API_V1: ApiSettings = ApiSettings()


@lru_cache
def get_settings() -> Settings:
    return Settings()


APP_SETTINGS = get_settings()
