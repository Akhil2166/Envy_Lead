from functools import lru_cache
from pathlib import Path
from typing import Literal

from pydantic import SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict

BACKEND_DIR = Path(__file__).resolve().parents[2]


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=BACKEND_DIR / ".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )

    app_name: str = "EnvyLead API"
    app_version: str = "0.1.0"
    environment: Literal["development", "test", "production"] = "development"
    debug: bool = False

    api_prefix: str = "/api"
    cors_origins: list[str] = [
        "http://localhost:5173",
        "http://127.0.0.1:5173",
        "https://envylead.vercel.app",
    ]

    database_url: str = "sqlite:///./envylead.db"

    gnani_api_key: SecretStr | None = None
    gnani_base_url: str = "https://api.vachana.ai"
    gnani_stt_model: str = "prisma-v3.0"
    gnani_tts_model: str = "timbre-v3.0"
    gnani_tts_voice: str = "Shivani"


@lru_cache
def get_settings() -> Settings:
    return Settings()
