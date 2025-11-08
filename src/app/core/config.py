from pydantic_settings import BaseSettings,SettingsConfigDict

class Settings(BaseSettings):
    db_engine: str
    db_port: str
    db_host: str
    db_user: str
    db_password: str
    db_name: str
    api_key: str

    model_config = SettingsConfigDict(env_file='.env', env_file_encoding='utf-8')

APP_CONFIG = dict(
    title="payment backend",
    description="API for managing a payment backend application.",
    version="1.0.0"
)

 