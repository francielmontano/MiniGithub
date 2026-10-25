from pydantic_settings import BaseSettings, SettingsConfigDict
from pathlib import Path

CONFIG_DIR = Path(__file__).parent.parent.parent
ENV_FILE = CONFIG_DIR / ".env"


class Settings(BaseSettings):
    
    # App Docs
    app_name: str = "Mini Github Project"
    app_version: str = "0.1.0"
    enviroment: str = "development"
    api_v1_prefix: str = ""
    
    # Data Base url
    database_url: str
    
    model_config = SettingsConfigDict(
        env_file = str(ENV_FILE),
        env_file_encoding = "utf-8",
        case_sensitive = False,
        extra = "ignore"
    )

# Instancia de configuracion. (Solo importar esto)

settings = Settings()