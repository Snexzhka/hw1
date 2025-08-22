from pydantic.v1 import BaseSettings



class Setting(BaseSettings):
    
    model_config = SettingsConfigDict(
        config_file=""
    )
