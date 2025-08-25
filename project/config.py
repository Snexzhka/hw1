from pydantic_settings import BaseSettings as PydanticSettings
from pydantic_settings import SettingsConfigDict


class Settings(PydanticSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )
