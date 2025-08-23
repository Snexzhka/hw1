from pydantic.v2 import BaseSettings



class Setting(BaseSettings):
    
    model_config = SettingsConfigDict(
        config_file=" ", 
        env_file = ".env", 
        env_file_encoding = "utf-8", 
    )
