from __future__ import annotations

from sqlalchemy import event
from sqlalchemy.engine import Engine
from sqlalchemy.ext.asyncio import (AsyncEngine, AsyncSession,
                                    create_async_engine)
from sqlalchemy.orm import declarative_base, sessionmaker

from ..config import settings

DATABASE_URL = f"sqlite+aiosqlite:///{settings.database_path}"

engine: AsyncEngine = create_async_engine(
    DATABASE_URL,
    future=True,
    echo=False,
    connect_args={"timeout": 30},
)

async_session = sessionmaker(
    bind=engine,
    expire_on_commit=False,
    class_=AsyncSession,
)

Base = declarative_base()

# Import models to ensure they are registered with SQLAlchemy metadata.
from ..models import AuditLog, PasswordEntry, User, Vault  # noqa: F401


async def init_db() -> None:
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


@event.listens_for(Engine, "connect")
def _set_sqlcipher_pragma(dbapi_connection, connection_record):
    if settings.enable_sqlcipher:
        cursor = dbapi_connection.cursor()
        # SQLCipher uses PRAGMA key to encrypt/decrypt the database.
        cursor.execute(f"PRAGMA key = '{settings.database_key.get_secret_value()}';")
        cursor.execute("PRAGMA cipher_page_size = 4096;")
        cursor.execute("PRAGMA kdf_iter = 64000;")
        cursor.execute("PRAGMA cipher_hmac_algorithm = HMAC_SHA512;")
        cursor.execute("PRAGMA cipher_kdf_algorithm = PBKDF2_HMAC_SHA512;")
        cursor.close()
