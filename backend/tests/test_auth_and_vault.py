import asyncio
import os
from pathlib import Path

# Use a dedicated test database path so tests start from a clean state.
TEST_DB_PATH = Path(__file__).resolve().parents[1] / "test_securepass.db"
if TEST_DB_PATH.exists():
    TEST_DB_PATH.unlink()
os.environ["DATABASE_PATH"] = str(TEST_DB_PATH)
os.environ["ENABLE_SQLCIPHER"] = "0"

from backend.app.database.connection import async_session, init_db
from backend.app.services.password import (hash_master_password,
                                           verify_master_password)
from backend.app.services.vault import create_default_vault, create_user


def test_password_hash_and_verify():
    password = "Sup3rS3cr3tP@ssw0rd"
    hashed = hash_master_password(password)
    assert verify_master_password(hashed, password)
    assert not verify_master_password(hashed, "wrongpass")


def test_create_user_and_vault():
    async def run_test():
        await init_db()
        async with async_session() as session:
            user = await create_user("test@example.com", "Sup3rS3cr3tP@ssw0rd", session)
            assert user.email == "test@example.com"
            vault = await create_default_vault(user, session)
            assert vault.user_id == user.id
            assert vault.name == "General"

    asyncio.run(run_test())
