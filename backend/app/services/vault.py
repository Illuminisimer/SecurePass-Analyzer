from __future__ import annotations

import os
from datetime import datetime
from typing import Any

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from .analysis import PasswordStrengthAnalyzer
from .encryption import decrypt_value, encrypt_value, derive_key
from .password import hash_master_password, verify_master_password
from ..models.password_entry import PasswordEntry
from ..models.user import User
from ..models.vault import Vault

ANALYZER = PasswordStrengthAnalyzer()


async def create_user(email: str, master_password: str, session: AsyncSession) -> User:
    salt = os.urandom(32)
    password_hash = hash_master_password(master_password)
    user = User(
        email=email,
        master_password_hash=password_hash,
        master_password_salt=salt,
    )
    session.add(user)
    await session.commit()
    await session.refresh(user)
    return user


async def get_user_by_email(email: str, session: AsyncSession) -> User | None:
    result = await session.execute(select(User).where(User.email == email))
    return result.scalars().first()


async def create_default_vault(user: User, session: AsyncSession) -> Vault:
    vault = Vault(user_id=user.id, name="General")
    session.add(vault)
    await session.commit()
    await session.refresh(vault)
    return vault


async def create_vault(user: User, name: str, description: str | None, session: AsyncSession) -> Vault:
    vault = Vault(user_id=user.id, name=name, description=description)
    session.add(vault)
    await session.commit()
    await session.refresh(vault)
    return vault


async def get_vaults_for_user(user: User, session: AsyncSession) -> list[Vault]:
    result = await session.execute(select(Vault).where(Vault.user_id == user.id))
    return result.scalars().all()


async def get_vault_entries(vault: Vault, session: AsyncSession) -> list[PasswordEntry]:
    result = await session.execute(select(PasswordEntry).where(PasswordEntry.vault_id == vault.id))
    return result.scalars().all()


async def create_password_entry(
    user: User,
    vault: Vault,
    title: str,
    url: str | None,
    username: str | None,
    password: str,
    notes: str | None,
    master_password: str,
    session: AsyncSession,
) -> PasswordEntry:
    key = derive_key(master_password, user.master_password_salt)
    encrypted_password = encrypt_value(password, key)
    encrypted_notes = encrypt_value(notes or "", key) if notes else None
    analysis = ANALYZER.analyze_password(password, username=username)
    entry = PasswordEntry(
        vault_id=vault.id,
        title=title,
        url=url,
        username=username,
        password_ciphertext=encrypted_password["ciphertext"].encode("utf-8"),
        password_nonce=encrypted_password["nonce"].encode("utf-8"),
        password_tag=encrypted_password["tag"].encode("utf-8"),
        notes_ciphertext=encrypted_notes["ciphertext"].encode("utf-8") if encrypted_notes else None,
        notes_nonce=encrypted_notes["nonce"].encode("utf-8") if encrypted_notes else None,
        notes_tag=encrypted_notes["tag"].encode("utf-8") if encrypted_notes else None,
        strength_score=analysis["score"],
        breach_status="BREACHED" if analysis["common_password"] else "CLEAN",
        tags="",
        folder_path="",
    )
    session.add(entry)
    await session.commit()
    await session.refresh(entry)
    return entry


async def decrypt_password_entry(entry: PasswordEntry, master_password: str, user: User) -> str:
    key = derive_key(master_password, user.master_password_salt)
    return decrypt_value(
        entry.password_ciphertext.decode("utf-8"),
        entry.password_nonce.decode("utf-8"),
        entry.password_tag.decode("utf-8"),
        key,
    )
