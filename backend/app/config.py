from __future__ import annotations

import os
from pathlib import Path

from pydantic import SecretStr, ConfigDict
from pydantic_settings import BaseSettings

BASE_DIR = Path(__file__).resolve().parents[2]


def _default_secret() -> str:
    return os.getenv("JWT_SECRET_KEY", "change-me-and-secure-this")


class Settings(BaseSettings):
    model_config = ConfigDict(
        env_file=BASE_DIR / ".env",
        env_file_encoding="utf-8",
    )
    app_name: str = "SecurePass Analyzer"
    database_path: str = str(BASE_DIR / "securepass.db")
    database_key: SecretStr = SecretStr(os.getenv("DATABASE_KEY", ""))
    jwt_secret_key: SecretStr = SecretStr(_default_secret())
    jwt_algorithm: str = "HS256"
    access_token_expire_minutes: int = 30
    argon2_time_cost: int = 3
    argon2_memory_cost: int = 65536
    argon2_parallelism: int = 4
    argon2_hash_len: int = 32
    argon2_salt_len: int = 32
    db_kdf_iterations: int = 64000
    openai_api_key: SecretStr = SecretStr(os.getenv("OPENAI_API_KEY", ""))
    openai_model: str = os.getenv("OPENAI_MODEL", "gpt-4o-mini")
    enable_sqlcipher: bool = True

settings = Settings()
