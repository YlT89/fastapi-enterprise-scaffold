from pydantic_settings import BaseSettings, SettingsConfigDict

class GlobalSettings(BaseSettings):
    app: str = 'dev'
    db_url: str = 'sqlite:///./dev1.db'
    cors_origins: list[str] = ["http://localhost:5173", "http://127.0.0.1:5173"]
    secret_key: str = "your_super_secret_key"
    token_expire_min: int = 30

    model_config = SettingsConfigDict(env_file=".env7")

settings = GlobalSettings()