# D:\Scaler-Agent-Replicator\agent\config.py
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    openai_api_key: str | None = None
    asana_email: str | None = None
    asana_password: str | None = None
    frontend_port: int = 3000
    backend_port: int = 8000
    use_llm: bool = False  # toggle

    model_config = SettingsConfigDict(
        env_file=".env",
        extra="ignore",
    )

settings = Settings()
