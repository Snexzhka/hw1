from pydantic import BaseSettings
from pydantic_settings import BaseSettings as PydanticSettings

class Settings(BaseSettings):
    
    model_config = SettingsConfigDict(
        config_file=" ", 
        env_file = ".env", 
        env_file_encoding = "utf-8", 
    )
