from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    database_url: str
    backend_port: int = 8000

    # If .env is in project root (D:\Scaler-Agent-Replicator\.env)
    model_config = SettingsConfigDict(
        env_file="../.env",
        extra="ignore",
    )

settings = Settings()
